"""Đếm khảo sát theo evidence/survey/cach-dem.md. Chỉ dùng thư viện chuẩn.

    python evidence/survey/count.py "file CSV tải từ Google Sheets"     lần đầu: ghi results.csv và summary.md
    python evidence/survey/count.py evidence/survey/results.csv        chạy lại trên bản đã bỏ cột nhận dạng

results.csv không có dấu thời gian và email; câu tự viết chỉ giữ khi người trả lời đồng ý cho trích;
email, số điện thoại và tên sự kiện nhận ra người viết được thay bằng chữ trong ngoặc vuông.
"""
import collections
import csv
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
# mã cột → (cụm trong tiêu đề của form, lần xuất hiện thứ mấy)
CAU = [
    ("truong_hop", "thuộc trường hợp nào", 0),
    ("noi_di", "khởi hành từ đâu", 0),
    ("do_dai", "kéo dài bao lâu", 0),
    ("thoi_gian_tim", "tổng cộng khoảng bao lâu", 0),
    ("su_co", "việc nào đã xảy ra", 0),
    ("tien", "so với dự tính", 0),
    ("cau_ke", "chia sẻ một tình huống", 0),
    ("cho_trich_ke", "được trích câu chia sẻ", 0),
    ("can_nhac", "đang cân nhắc", 0),
    ("muon_biet", "muốn biết điều gì nhất", 0),
    ("cau_hoi", "đang muốn hỏi điều gì", 0),
    ("cho_trich_hoi", "được trích câu chia sẻ", 1),
]
SU_CO = [("Đến nơi mới biết đóng cửa hoặc hết giờ nhận khách", "đóng cửa"),
         ("Đi vòng hoặc quay lại do cách xếp lịch", "đi vòng"),
         ("Đổi lịch vì thông tin sai hoặc chưa rõ", "đổi lịch vì thông tin")]
THOI_GIAN = [("Dưới 30 phút", "dưới 30", 15), ("30 phút đến dưới 1 giờ", "từ 30 phút", 45),
             ("1 đến 3 giờ", "1 đến 3", 120), ("Hơn 3 giờ", "hơn 3", 240)]
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
SDT = re.compile(r"(?<!\d)(?:\+?84|0)(?:[\s.-]?\d){8,10}(?!\d)")
SU_KIEN = re.compile(r"(?i)(?<=lúc đi )thi .+?(?= em )")


def chuan(text):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", str(text or ""))).strip().lower()


def che(text):
    text = SU_KIEN.sub("[một cuộc thi]", unicodedata.normalize("NFC", (text or "").strip()))
    return SDT.sub("[số điện thoại]", EMAIL.sub("[email]", text))


def doc(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    header, data = rows[0], [r for r in rows[1:] if any(c.strip() for c in r)]
    codes = [c for c, _, _ in CAU]
    if all(c in header for c in codes):  # đã là results.csv
        return [{c: r[header.index(c)] for c in codes} for r in data]
    index = {}
    for code, phrase, nth in CAU:
        found = [i for i, h in enumerate(header) if phrase in chuan(h)]
        if len(found) <= nth:
            raise SystemExit("Không thấy câu hỏi có cụm '%s'. Tiêu đề đang có:\n  %s" % (phrase, "\n  ".join(header)))
        index[code] = found[nth]
    out = []
    for r in data:
        item = {c: che(r[i]) if i < len(r) else "" for c, i in index.items()}
        known = ("đóng cửa hoặc đã hết giờ", "đi vòng hoặc quay lại", "đổi lịch vì thông tin", "không gặp các việc", "không nhớ rõ")
        if chuan(item["cho_trich_ke"]) != "đồng ý" and item["su_co"] and not any(k in chuan(item["su_co"]) for k in known):
            item["su_co"] = "[mục khác]"
        for text, consent in (("cau_ke", "cho_trich_ke"), ("cau_hoi", "cho_trich_hoi")):
            if chuan(item[consent]) != "đồng ý":
                item[text] = ""
        out.append(item)
    return out


def da_chuan_bi(r):
    t = chuan(r["truong_hop"])
    return "có tham gia chuẩn bị" in t


def tu_noi_khac(r):
    t = chuan(r["noi_di"])
    return "hcm" in t or "tỉnh/thành khác" in t


def tu_hcm(r):
    return "hcm" in chuan(r["noi_di"])


def lan_dau(r):
    return "một lần" in chuan(r["truong_hop"])


def dem(group, field, needle):
    return sum(needle in chuan(r[field]) for r in group)


def so_lieu(rows):
    trip = [r for r in rows if da_chuan_bi(r)]
    main = [r for r in trip if tu_noi_khac(r)]
    groups = [("Mẫu chính: đi từ ngoài Hà Nội, có chuẩn bị", main),
              ("Trong đó đi từ TP.HCM", [r for r in main if tu_hcm(r)]),
              ("Trong đó từ TP.HCM và mới đi một lần", [r for r in main if tu_hcm(r) and lan_dau(r)])]
    table = [("Gặp ít nhất một việc ở câu 5", [sum(any(n in chuan(r["su_co"]) for _, n in SU_CO) for r in g) for _, g in groups])]
    table += [(label, [dem(g, "su_co", n) for _, g in groups]) for label, n in SU_CO]
    table += [("Chi cao hơn dự tính", [dem(g, "tien", "cao hơn dự tính") for _, g in groups]),
              ("Trong đó cao hơn trên 200.000 đ", [dem(g, "tien", "trên 200") for _, g in groups]),
              ("Tìm thông tin từ 1 giờ trở lên", [dem(g, "thoi_gian_tim", "1 đến 3") + dem(g, "thoi_gian_tim", "hơn 3") for _, g in groups])]
    minutes = [next((m for _, n, m in THOI_GIAN if n in chuan(r["thoi_gian_tim"])), None) for r in main]
    minutes = [m for m in minutes if m is not None]
    return trip, groups, table, minutes


def tom_tat(rows):
    trip, groups, table, minutes = so_lieu(rows)
    main = groups[0][1]
    n = len(main)
    other = [r for r in rows if not da_chuan_bi(r)]
    lines = [
        "# Kết quả khảo sát",
        "",
        "Cách đếm: `cach-dem.md`. Câu hỏi: `questions.md`. Dữ liệu: `results.csv`. "
        "Chạy lại: `python evidence/survey/count.py evidence/survey/results.csv`.",
        "",
        "- Tổng câu trả lời: **%d**" % len(rows),
        "- Có đi Hà Nội và có chuẩn bị chuyến đi: %d · trong đó đang ở sẵn Hà Nội (không vào mẫu): %d" % (len(trip), len(trip) - n),
        "- Chưa đi hoặc không tự chuẩn bị (chỉ trả lời câu về nhu cầu): %d" % len(other),
        "- **Mẫu chính N = %d.** Ngưỡng khảo sát là ≥20 người đúng người dùng: **%s**."
        % (n, "đạt" if n >= 20 else "chưa đạt, thiếu %d" % (20 - n)),
        "",
        "| Đếm gì | %s |" % " | ".join("%s (N = %d)" % (name, len(g)) for name, g in groups),
        "|---|%s" % ("---|" * len(groups)),
    ]
    lines += ["| %s | %s |" % (label, " | ".join("%d/%d" % (v, len(g)) for v, (_, g) in zip(values, groups))) for label, values in table]
    if n >= 20:
        lines += ["", "Mốc đặt trước ≥20%% người gặp ít nhất một việc: %s (%.1f%%)."
                  % ("đạt" if table[0][1][0] >= 0.2 * n else "không đạt", 100.0 * table[0][1][0] / n)]
    else:
        lines += ["", "N dưới 20 nên chỉ ghi x/N, không ghi phần trăm."]
    lines += ["", "## Thời gian tìm thông tin (mẫu chính)", "", "| Chọn | Số người | Phút giữa khoảng *(tự ước tính)* |", "|---|---|---|"]
    lines += ["| %s | %d/%d | %d |" % (label, dem(main, "thoi_gian_tim", needle), n, mid) for label, needle, mid in THOI_GIAN]
    if minutes:
        lines += ["", "Trung bình theo phút giữa khoảng: **%d phút** trên %d người. Dùng cho `spec.md` §2."
                  % (int(sum(minutes) / len(minutes) + 0.5), len(minutes))]
    want = collections.Counter(r["muon_biet"].strip() for r in other if r["muon_biet"].strip())
    lines += ["", "## Người đang cân nhắc đi (ngoài mẫu chính, %d người trả lời câu muốn biết nhất)" % sum(want.values()), ""]
    lines += ["- %s %d" % (k, v) for k, v in want.most_common()] or ["Chưa có."]
    lines += ["", "## Câu kể nguyên văn của mẫu chính (đã đồng ý cho trích)", ""]
    quotes = [r["cau_ke"].strip() for r in main if r["cau_ke"].strip()]
    lines += ["%d. \"%s\"" % (i, q) for i, q in enumerate(quotes, 1)] or ["Chưa có."]
    asked = [r["cau_hoi"].strip() for r in other if r["cau_hoi"].strip()]
    lines += ["", "## Câu hỏi của người đang cân nhắc (đã đồng ý cho trích)", ""]
    lines += ["%d. \"%s\"" % (i, q) for i, q in enumerate(asked, 1)] or ["Chưa có."]
    return "\n".join(lines) + "\n"


def main(argv):
    if len(argv) != 1 or not os.path.exists(argv[0]):
        print(__doc__)
        return 2
    rows = doc(argv[0])
    out = os.path.join(HERE, "results.csv")
    if os.path.abspath(argv[0]) != out:
        with open(out, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=[c for c, _, _ in CAU])
            w.writeheader()
            w.writerows(rows)
    text = tom_tat(rows)
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
