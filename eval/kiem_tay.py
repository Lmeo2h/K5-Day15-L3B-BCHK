"""Phiếu người chấm lượt 1 (metric_spec.yaml: kiểm tay mọi câu trượt và ít nhất 5 câu đạt).

    python eval/kiem_tay.py        tạo eval/kiem_tay_run1.csv (không có điểm AI) và bản đọc eval/kiem_tay_run1.md
    python eval/kiem_tay.py so     sau khi điền cột nguoi_cham (1 / 0): in số câu khớp với cột pass của lượt 1

Không sửa eval/run-1.csv.
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.join(HERE, "run-1.csv")
SHEET = os.path.join(HERE, "kiem_tay_run1.csv")
DOC = os.path.join(HERE, "kiem_tay_run1.md")
HIEU_CHUAN = ["B04", "B06", "B08", "B10", "B17"]  # 5 output người thứ hai chấm thử (eval/README.md mục 3)
THEM_CAU_DAT = ["B02", "B13"]


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def chon(rows):
    """Mọi câu trượt, 5 câu hiệu chuẩn và vài câu đạt thêm; xếp theo mã để người chấm không đoán được."""
    ids = {r["id"] for r in rows if r["pass"] == "0"} | set(HIEU_CHUAN) | set(THEM_CAU_DAT)
    return [r for r in rows if r["id"] in ids]


def tao():
    if os.path.exists(SHEET):
        print("Đã có %s, không ghi đè." % SHEET)
        return 1
    picked = chon(read_csv(RUN))
    with open(SHEET, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "type", "nguoi_cham", "ly_do"])
        w.writerows([r["id"], r["type"], "", ""] for r in picked)
    out = ["# Phiếu chấm tay lượt 1 (%d câu)" % len(picked), "",
           "Điền 1 hoặc 0 vào cột `nguoi_cham` của `kiem_tay_run1.csv`. Đạt khi output thoả **mọi ý** của tiêu chí; "
           "output có lịch thì không được trùng ngày đóng cửa hay vượt trần. Chưa xong thì đừng mở `run-1.csv`."]
    for r in picked:
        out += ["", "## %s (%s)" % (r["id"], r["type"]), "", "**Input:** " + r["input"], "",
                "**Tiêu chí:** " + r["pass_criterion"], "", "```", r["output"] or r["error"], "```"]
    with open(DOC, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("Đã tạo %s (%d câu) và %s" % (SHEET, len(picked), DOC))
    return 0


def so():
    ai = {r["id"]: r["pass"] for r in read_csv(RUN)}
    sheet = read_csv(SHEET)
    done = [r for r in sheet if r["nguoi_cham"].strip() in ("0", "1")]
    if not done:
        print("Phiếu chưa điền cột nguoi_cham.")
        return 1
    for name, group in (("Tất cả", done), ("5 output hiệu chuẩn", [r for r in done if r["id"] in HIEU_CHUAN])):
        same = [r for r in group if r["nguoi_cham"].strip() == ai[r["id"]]]
        print("%s: đã chấm %d, khớp %d/%d" % (name, len(group), len(same), len(group)))
    for r in done:
        if r["nguoi_cham"].strip() != ai[r["id"]]:
            print("  lệch %s: người %s · AI %s · %s" % (r["id"], r["nguoi_cham"], ai[r["id"]], r["ly_do"]))
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    sys.exit(so() if sys.argv[1:] == ["so"] else tao())
