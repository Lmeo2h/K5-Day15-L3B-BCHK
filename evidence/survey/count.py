"""Đếm khảo sát theo evidence/survey/cach-dem.md. Chỉ dùng thư viện chuẩn.

    python evidence/survey/count.py "đường dẫn file CSV xuất từ Google Forms"

Ghi results.csv (đã bỏ cột nhận dạng) và summary.md cạnh file này, in tóm tắt ra màn hình.
Chạy lại trên results.csv cũng được.
"""
import csv
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
# mã cột → các cụm nhận ra câu hỏi trong tiêu đề cột của Google Forms
CAU = {
    "q1_xuat_phat": ["xuất phát"],
    "q2_khi_nao": ["chuyến đó là khi nào", "khi nào"],
    "q3_kieu_di": ["đi kiểu gì", "kiểu gì"],
    "q4_thoi_gian": ["bao lâu"],
    "q5_nguon": ["xem thông tin"],
    "q6_su_co": ["điều nào đã xảy ra", "đã xảy ra"],
    "q7_tong_tien": ["tổng tiền"],
    "q8_ke": ["khó chịu nhất", "kể ngắn"],
}
BAT_BUOC = ("q1_xuat_phat", "q6_su_co")
SU_CO = [("Đến nơi thì đóng cửa", "đóng cửa"), ("Đi vòng vì các điểm xa nhau", "đi vòng"),
         ("Trả cao hơn dự kiến", "trả cao hơn"), ("Không biết đi gì từ sân bay, bến xe", "không biết đi")]
PHUT = [("không lên lịch", 0), ("dưới 1", 30), ("trên 3", 240), ("1-3", 120), ("1 - 3", 120), ("1–3", 120)]
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
SDT = re.compile(r"(?<!\d)(?:\+?84|0)(?:[\s.-]?\d){8,10}(?!\d)")


def chuan(text):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", str(text or ""))).strip().lower()


def che(text):
    return SDT.sub("[số điện thoại]", EMAIL.sub("[email]", (text or "").strip()))


def doc(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        rows = list(reader)
    cot = {}
    for ma, cum in CAU.items():
        if ma in header:
            cot[ma] = ma
            continue
        for c in cum:
            found = [h for h in header if c in chuan(h) and h not in cot.values()]
            if found:
                cot[ma] = found[0]
                break
    thieu = [m for m in BAT_BUOC if m not in cot]
    if thieu:
        raise SystemExit("Không nhận ra cột: %s.\nTiêu đề đang có:\n  %s\nSửa danh sách cụm từ CAU trong count.py."
                         % (", ".join(thieu), "\n  ".join(header)))
    out, seen = [], set()
    for r in rows:
        item = {ma: che(r.get(cot[ma], "")) if ma in cot else "" for ma in CAU}
        key = tuple(chuan(v) for v in item.values())
        if any(key) and key not in seen:
            seen.add(key)
            out.append(item)
    return out, [m for m in CAU if m not in cot], len(rows)


def du_dieu_kien(r):
    q1 = chuan(r["q1_xuat_phat"])
    if "sống ở hà nội" in q1 or "chưa đến" in q1 or "chưa đi" in q1:
        return False
    return any(x in q1 for x in ("hcm", "hồ chí minh", "sài gòn", "tỉnh khác", "tỉnh"))


def tom_tat(rows, thieu, tho):
    mau = [r for r in rows if du_dieu_kien(r)]
    n = len(mau)

    def ti(x):
        if not n:
            return "0/0"
        return "%d/%d (%s%%)" % (x, n, ("%.1f" % (100.0 * x / n)).replace(".", ",")) if n >= 20 else "%d/%d" % (x, n)

    def dem(ma, cum):
        return sum(cum in chuan(r[ma]) for r in mau)

    any_issue = sum(any(c in chuan(r["q6_su_co"]) for _, c in SU_CO) for r in mau)
    hcm = sum(any(x in chuan(r["q1_xuat_phat"]) for x in ("hcm", "hồ chí minh", "sài gòn")) for r in mau)
    gan = sum(any(x in chuan(r["q2_khi_nao"]) for x in ("1 tháng", "1-12", "1 - 12", "1–12")) for r in mau)
    phut = []
    for r in mau:
        q4 = chuan(r["q4_thoi_gian"])
        value = next((v for c, v in PHUT if c in q4), None)
        if value is not None:
            phut.append(value)
    vuot = dem("q7_tong_tien", "vượt")
    dat = n >= 20
    lines = [
        "# Kết quả khảo sát",
        "",
        "Cách đếm: `cach-dem.md`. Dữ liệu: `results.csv`. Chạy lại: `python evidence/survey/count.py evidence/survey/results.csv`.",
        "",
        "- Dòng trong file xuất: %d · sau khi bỏ trùng: %d · đủ điều kiện (N): **%d** (từ TP.HCM: %d)" % (tho, len(rows), n, hcm),
        "- Chuyến trong 12 tháng qua: %s" % ti(gan),
        "- Ngưỡng ≥20 người: **%s**" % ("đạt" if dat else "chưa đạt (mới %d)" % n),
        "",
        "| Đếm gì | Kết quả |",
        "|---|---|",
        "| Gặp ít nhất một sự cố | **%s** |" % ti(any_issue),
    ]
    lines += ["| %s | %s |" % (label, ti(dem("q6_su_co", c))) for label, c in SU_CO]
    lines += ["| Chi vượt dự tính | %s |" % ti(vuot)]
    if phut:
        lines += ["| Thời gian lên lịch trung bình | %d phút (trên %d người trả lời, giá trị giữa khoảng là tự ước tính) |"
                  % (round(sum(phut) / len(phut)), len(phut))]
    if dat:
        rate = 100.0 * any_issue / n
        lines += ["", "Mốc đặt trước ≥20%%: **%s** (%s%%)." % ("đạt" if rate >= 20 else "không đạt",
                                                              ("%.1f" % rate).replace(".", ","))]
    ke = [r["q8_ke"] for r in mau if len(chuan(r["q8_ke"])) >= 8]
    lines += ["", "## Câu kể nguyên văn (mọi câu có nội dung, đọc lại trước khi commit)", ""]
    lines += ["%d. \"%s\"" % (i, re.sub(r"\s+", " ", k)) for i, k in enumerate(ke, 1)] or ["Chưa có."]
    if thieu:
        lines += ["", "Không thấy cột: %s." % ", ".join(thieu)]
    return "\n".join(lines) + "\n"


def main(argv):
    if len(argv) != 1 or not os.path.exists(argv[0]):
        print(__doc__)
        return 2
    rows, thieu, tho = doc(argv[0])
    out = os.path.join(HERE, "results.csv")
    if os.path.abspath(argv[0]) != out:
        with open(out, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(CAU))
            w.writeheader()
            w.writerows(rows)
    text = tom_tat(rows, thieu, tho)
    with open(os.path.join(HERE, "summary.md"), "w", encoding="utf-8") as f:
        f.write(text)
    print(text)
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    sys.exit(main(sys.argv[1:]))
