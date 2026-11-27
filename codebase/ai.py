"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str, schema=None, effort=None) -> dict với 4 khoá
    (schema: JSON schema ép định dạng; effort: mức suy luận minimal / low / medium của model gpt-5)
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.
    Lỗi gọi model (hết lượt, sai key, mất mạng): cứ để exception bay ra — khung ghi lỗi vào cột error.

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER, hoặc MODEL_PROVIDER=fake):
    trả một câu giả cố định, model "fake", token 0.

Nối model thật: .env đặt MODEL_PROVIDER=openai, MODEL_NAME, API_KEY. API_BASE để trống = api.openai.com.
Chỉ điền API_BASE khi key thuộc một dịch vụ tương thích OpenAI và bạn tin dịch vụ đó. Không dán API key vào file này.
"""
import json
import os
import time
import urllib.error
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()
API_BASE = (os.environ.get("API_BASE") or "https://api.openai.com/v1").strip().rstrip("/")
RETRY_WAIT = (5, 15)  # giây chờ khi bị giới hạn lượt (429) hoặc máy chủ lỗi


def post_json(url, headers, body, timeout=90):
    """Gửi POST JSON, trả về JSON phản hồi. Chỉ dùng thư viện chuẩn."""
    data = json.dumps(body).encode("utf-8")
    for wait in RETRY_WAIT + (None,):
        req = urllib.request.Request(url, data=data, method="POST",
                                     headers=dict({"Content-Type": "application/json"}, **headers))
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if wait is not None and e.code in (429, 500, 502, 503):
                time.sleep(wait)
                continue
            msg = e.read().decode("utf-8", "replace")[:300]
            if API_KEY:
                msg = msg.replace(API_KEY, "<key>")
            raise RuntimeError("HTTP %d: %s" % (e.code, msg))


def call_openai(system, user, schema=None, effort=None):
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    body = {"model": MODEL_NAME, "messages": messages, "response_format": {"type": "json_object"}}
    if schema:  # structured outputs: model chỉ trả được giá trị nằm trong schema
        body["response_format"] = {"type": "json_schema",
                                   "json_schema": {"name": "ket_qua", "strict": True, "schema": schema}}
    effort = (os.environ.get("REASONING_EFFORT") or "").strip() or effort
    if effort and MODEL_NAME.startswith("gpt-5"):  # chỉ model suy luận nhận tham số này
        body["reasoning_effort"] = effort
    data = post_json(API_BASE + "/chat/completions", {"Authorization": "Bearer " + API_KEY}, body)
    usage = data["usage"]
    return {"text": data["choices"][0]["message"]["content"] or "",
            "tokens_in": usage["prompt_tokens"], "tokens_out": usage["completion_tokens"]}


@model_call
def call_model(system: str, user: str, schema: dict = None, effort: str = None) -> dict:
    if MODEL_PROVIDER == "fake":
        last = (user.strip().splitlines() or [""])[-1]
        return {"text": "[câu trả lời giả — chưa nối model] " + last[:60], "model": "fake", "tokens_in": 0, "tokens_out": 0}
    if MODEL_PROVIDER != "openai":
        raise NotImplementedError("codebase/ai.py mới hỗ trợ MODEL_PROVIDER=openai (hoặc fake), đang là %s" % MODEL_PROVIDER)
    if not API_KEY or not MODEL_NAME:
        raise RuntimeError("thiếu API_KEY hoặc MODEL_NAME trong .env")
    r = call_openai(system, user, schema, effort)
    return {"text": r["text"], "model": MODEL_NAME, "tokens_in": int(r["tokens_in"]), "tokens_out": int(r["tokens_out"])}
