"""Xuất slides/demo-slides.html thành demo-slides.pdf ở thư mục gốc, dùng Edge hoặc Chrome không màn hình.

    python slides/build.py
"""
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "slides" / "demo-slides.html"
OUTPUT = ROOT / "demo-slides.pdf"
CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]


def browser():
    for path in CANDIDATES:
        if os.path.exists(path):
            return path
    for name in ("msedge", "google-chrome", "chromium", "chromium-browser"):
        found = shutil.which(name)
        if found:
            return found
    raise SystemExit("Không tìm thấy Edge hoặc Chrome. Mở slides/demo-slides.html rồi in ra PDF, bật 'đồ hoạ nền'.")


def main():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as work:
        draft = Path(work) / "slides.pdf"
        subprocess.run([browser(), "--headless=new", "--user-data-dir=" + str(Path(work) / "profile"), "--no-first-run",
                        "--no-pdf-header-footer", "--virtual-time-budget=5000",
                        "--print-to-pdf=" + str(draft), SOURCE.as_uri()],
                       check=True, timeout=120, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # trên Windows lệnh trả về trước khi file được ghi xong: chờ tới khi file kết thúc bằng %%EOF
        deadline = time.time() + 90
        while not (draft.exists() and b"%%EOF" in draft.read_bytes()[-64:]):
            if time.time() > deadline:
                raise SystemExit("Trình duyệt không ghi ra file PDF.")
            time.sleep(0.5)
        shutil.copyfile(draft, OUTPUT)
    print("Đã ghi %s (%.0f KB)" % (OUTPUT, OUTPUT.stat().st_size / 1024))
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    sys.exit(main())
