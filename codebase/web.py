"""Giao diện web chạy trên máy. Chỉ dùng thư viện chuẩn.

    python run.py                      mở http://127.0.0.1:8000
    python codebase/web.py --no-browser --port 8010

API:
    GET  /api/meta            chế độ (thật / giả), model, danh sách khu ở và sở thích
    POST /api/lich {"text"}   chạy answer() trong khung trace, trả kết quả và dữ liệu để vẽ

An toàn: chỉ nghe trên 127.0.0.1; từ chối Host và Origin lạ (trang web khác không gọi hộ được để tốn token);
chỉ phục vụ đúng các file trong ui/; API key nằm ở phía máy chủ, lỗi trả về trình duyệt không kèm chi tiết.
"""
import json
import os
import sys
import threading
import time
import urllib.error
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import ai  # noqa: E402
import tools  # noqa: E402
import tracing  # noqa: E402
import view  # noqa: E402
from agent import answer  # noqa: E402

UI = os.path.join(HERE, "ui")
FILES = {"/": ("index.html", "text/html"), "/app.css": ("app.css", "text/css"),
         "/app.js": ("app.js", "text/javascript"), "/favicon.svg": ("favicon.svg", "image/svg+xml")}
MAX_BODY = 8 * 1024
MAX_TEXT = 1000
WAIT_TURN_S = 120
# Khung trace dùng biến chung, nên mỗi lúc chỉ chạy một yêu cầu.
RUN_LOCK = threading.Lock()

LOI = {
    "mang": "Không kết nối được tới dịch vụ AI. Kiểm tra mạng rồi thử lại.",
    "khoa": "API key bị từ chối. Kiểm tra file .env trên máy chạy.",
    "het_luot": "Dịch vụ AI đang giới hạn lượt gọi. Đợi một lát rồi thử lại.",
    "cau_hinh": "Chưa cấu hình model đúng. Xem docs/connect-model.md.",
    "ban": "Đang xử lý một yêu cầu khác. Thử lại sau vài giây.",
    "he_thong": "Có lỗi khi xử lý yêu cầu. Chi tiết nằm ở cửa sổ lệnh đang chạy giao diện.",
}


def classify(error):
    text = str(error)
    if isinstance(error, (urllib.error.URLError, TimeoutError, ConnectionError)):
        return "mang"
    if isinstance(error, NotImplementedError) or "thiếu API_KEY" in text:
        return "cau_hinh"
    if text.startswith(("HTTP 401", "HTTP 403")):
        return "khoa"
    if text.startswith("HTTP 429"):
        return "het_luot"
    return "he_thong"


def _steps(events):
    """Các bước đã chạy, bỏ phần xem trước input / output."""
    keep = ("kind", "name", "model", "tokens_in", "tokens_out", "latency_s", "text")
    steps = [{k: e[k] for k in keep if k in e} for e in events]
    for step, event in zip(steps, events):
        step["loi"] = bool(event.get("error"))
    return steps


def run_once(text):
    """Chạy một yêu cầu. Gọi khi đang giữ RUN_LOCK."""
    start = time.perf_counter()
    tracing.begin("web")
    try:
        result = answer(text)
    finally:
        summary, events = tracing.end()
    return {"loai": result.get("loai"), "output": result.get("output", ""), "xem": view.build(result),
            "luot": {"model": ", ".join(summary["models"]), "goi_model": summary["model_calls"],
                     "goi_cong_cu": summary["tool_calls"], "token_vao": summary["tokens_in"],
                     "token_ra": summary["tokens_out"], "giay": round(time.perf_counter() - start, 1),
                     "buoc": _steps(events)}}


def meta():
    fake = ai.MODEL_PROVIDER == "fake"
    return {"gia": fake, "model": "chế độ giả" if fake else ai.MODEL_NAME, "ngay_du_lieu": tools.DATA_DATE,
            "toi_da": MAX_TEXT,
            "khu": [{"ma": k, "ten": v} for k, v in view.KHU.items()],
            "so_thich": [{"ma": k, "ten": v} for k, v in view.SO_THICH.items()]}


class Handler(BaseHTTPRequestHandler):
    server_version = "BCHK"
    sys_version = ""
    timeout = 30

    def log_message(self, fmt, *args):  # giữ cửa sổ lệnh gọn khi demo
        pass

    def _send(self, status, body, content_type="application/json"):
        if not isinstance(body, bytes):
            body = json.dumps(body, ensure_ascii=False).encode("utf-8")
        try:
            self.send_response(status)
            self.send_header("Content-Type", content_type + "; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy",
                             "default-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'none'; "
                             "form-action 'self'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionError):
            pass  # người dùng đã đóng hoặc tải lại trang

    def _fail(self, status, code, message=None):
        self._send(status, {"loi": code, "thong_bao": message or LOI.get(code, LOI["he_thong"])})

    def _local_only(self):
        port = self.server.server_address[1]
        allowed = {"127.0.0.1:%d" % port, "localhost:%d" % port}
        origin = self.headers.get("Origin")
        if self.headers.get("Host") not in allowed or (origin and origin not in {"http://" + h for h in allowed}):
            self._fail(403, "tu_choi", "Chỉ nhận yêu cầu từ giao diện chạy trên máy này.")
            return False
        return True

    def do_GET(self):
        if not self._local_only():
            return
        path = self.path.split("?", 1)[0]
        if path == "/api/meta":
            return self._send(200, meta())
        if path not in FILES:
            return self._fail(404, "khong_co", "Không có trang này.")
        name, content_type = FILES[path]
        try:
            with open(os.path.join(UI, name), "rb") as f:
                self._send(200, f.read(), content_type)
        except OSError:
            self._fail(500, "he_thong")

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = -1
        if not 0 <= length <= MAX_BODY:
            return self._fail(413, "qua_dai", "Yêu cầu quá dài.")
        raw = self.rfile.read(length)
        if not self._local_only():
            return
        if self.path != "/api/lich":
            return self._fail(404, "khong_co", "Không có địa chỉ này.")
        if (self.headers.get("Content-Type") or "").split(";")[0].strip().lower() != "application/json":
            return self._fail(415, "sai_dinh_dang", "Chỉ nhận JSON.")
        try:
            text = json.loads(raw.decode("utf-8"))["text"].strip()
        except (ValueError, KeyError, TypeError, AttributeError):
            return self._fail(400, "sai_dinh_dang", "Thiếu nội dung yêu cầu.")
        if not text:
            return self._fail(400, "trong", "Bạn chưa nhập yêu cầu.")
        if len(text) > MAX_TEXT:
            return self._fail(413, "qua_dai", "Yêu cầu dài quá %d ký tự." % MAX_TEXT)
        if not RUN_LOCK.acquire(timeout=WAIT_TURN_S):
            return self._fail(503, "ban")
        try:
            payload = run_once(text)
        except Exception as e:  # lỗi gọi model hoặc lỗi code: ghi ở cửa sổ lệnh, trình duyệt chỉ nhận loại lỗi
            print("[lỗi] %s: %s" % (type(e).__name__, e), file=sys.stderr, flush=True)
            return self._fail(502, classify(e))
        finally:
            RUN_LOCK.release()
        self._send(200, payload)


class Server(ThreadingHTTPServer):
    daemon_threads = True
    # Trên Windows, SO_REUSEADDR cho hai máy chủ cùng nghe một cổng, nên phải tắt để dò được cổng bận.
    allow_reuse_address = os.name != "nt"


def make_server(port=8000, tries=20):
    """Mở máy chủ ở cổng đầu tiên còn trống kể từ port."""
    last = None
    for candidate in range(port, port + tries):
        try:
            return Server(("127.0.0.1", candidate), Handler)
        except OSError as e:
            last = e
    raise OSError("không mở được cổng nào từ %d đến %d: %s" % (port, port + tries - 1, last))


def main(argv=()):
    argv = list(argv)
    port = 8000
    if "--port" in argv:
        try:
            port = int(argv[argv.index("--port") + 1])
        except (IndexError, ValueError):
            print("Cần số cổng sau --port, ví dụ: --port 8010")
            return 2
    try:
        server = make_server(port)
    except OSError as e:
        print("Không mở được giao diện: %s" % e)
        return 1
    url = "http://127.0.0.1:%d" % server.server_address[1]
    info = meta()
    print("Giao diện đang chạy tại %s" % url)
    print("Model: %s. Dừng bằng Ctrl+C. Bản dòng lệnh: python codebase/app.py --cli" % info["model"], flush=True)
    if "--no-browser" not in argv:
        threading.Timer(0.4, webbrowser.open, (url,)).start()
    try:
        server.serve_forever(poll_interval=0.3)
    except KeyboardInterrupt:
        print("\nĐã dừng.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    for _stream in (sys.stdout, sys.stderr):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    sys.exit(main(sys.argv[1:]))
