"""Bản chạy thử: giao diện web (mặc định) hoặc dòng lệnh. Cả hai đều gọi answer() trong agent.py.

    python run.py                    mở giao diện web ở http://127.0.0.1:8000 (xem web.py)
    python codebase/app.py --cli     bản dòng lệnh: gõ đầu vào → in kết quả

Khi đầu vào được đưa qua ống (vd: echo "..." | python run.py) thì tự dùng bản dòng lệnh; thêm --web để ép mở web.
"""
import os
import sys

for _stream in (sys.stdout, sys.stderr, sys.stdin):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _where(e):
    """File (trong codebase/) gây lỗi khi nạp: SyntaxError có e.filename, lỗi khác lấy khung cuối của traceback."""
    import traceback
    path = getattr(e, "filename", None) or (traceback.extract_tb(e.__traceback__)[-1].filename if e.__traceback__ else "")
    if not path:
        return "codebase/"
    p = os.path.abspath(path)
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.relpath(p, base).replace(os.sep, "/") if p.startswith(base) else path

def main(argv=()) -> int:
    if "--cli" in argv or ("--web" not in argv and not (sys.stdin and sys.stdin.isatty())):
        return cli()
    try:
        import web
    except Exception as e:  # lỗi trong codebase/: báo rõ chỗ, bản dòng lệnh vẫn thử được
        print("Không mở được giao diện web — lỗi ở %s: %s: %s" % (_where(e), type(e).__name__, e))
        print("Thử bản dòng lệnh: python codebase/app.py --cli")
        return 1
    return web.main([a for a in argv if a != "--web"])


def cli() -> int:
    try:
        import tracing
        from agent import answer
    except Exception as e:  # lỗi cú pháp, thiếu thư viện… trong codebase/
        print("Không nạp được codebase/ — lỗi ở %s: %s: %s" % (_where(e), type(e).__name__, e))
        print("Sửa lỗi rồi chạy lại. Cách nối model: docs/connect-model.md")
        return 1
    print("Bản chạy thử — gõ đầu vào rồi Enter. Thoát: Ctrl+C (hoặc Enter 2 lần với dòng trống).")
    blank = 0
    while True:
        try:
            text = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not text:
            blank += 1
            if blank >= 2:
                return 0
            continue
        blank = 0
        tracing.begin("app")
        try:
            result = answer(text)
        except NotImplementedError as e:
            tracing.end()
            print("Chưa nối model: %s" % e)
            return 1
        except Exception as e:  # lỗi gọi model: báo rồi cho hỏi tiếp
            tracing.end()
            print("[lỗi] %s: %s" % (type(e).__name__, e))
            continue
        s, _ = tracing.end()
        print(result.get("output", "") if isinstance(result, dict) else result)
        print("   (model: %s · gọi model %d lần · công cụ %d lần · token vào %d / ra %d)"
              % (", ".join(s["models"]) or "—", s["model_calls"], s["tool_calls"], s["tokens_in"], s["tokens_out"]))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
