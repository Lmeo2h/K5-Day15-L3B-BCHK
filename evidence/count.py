"""Đếm x/N từ bảng gắn nhãn evidence/voz-labels.csv. Chạy: python evidence/count.py"""
import csv
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

LABELS = ["L1_thong_tin", "L2_trai_tuyen", "L3_dong_cua", "L4_chi_phi"]
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz-labels.csv")
with open(path, encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))


def show(name, x, n):
    print("%-28s %3d/%-3d (%.1f%%)" % (name, x, n, 100.0 * x / n))


n = len(rows)
show("Bài nêu ít nhất 1 lỗi", sum(any(r[k] == "1" for k in LABELS) for r in rows), n)
for k in LABELS:
    show("  " + k, sum(r[k] == "1" for r in rows), n)
threads = sorted({r["thread_id"] for r in rows})
show("Thread có ít nhất 1 bài", sum(any(r["thread_id"] == t and any(r[k] == "1" for k in LABELS) for r in rows) for t in threads), len(threads))
for t in threads:
    sub = [r for r in rows if r["thread_id"] == t]
    show("  thread " + t, sum(any(r[k] == "1" for k in LABELS) for r in sub), len(sub))
