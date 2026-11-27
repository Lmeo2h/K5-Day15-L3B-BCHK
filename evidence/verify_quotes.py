"""Tải lại trang 1 của 5 thread và đối chiếu với evidence/voz-labels.csv, evidence/summary.md. Cần mạng.

    python evidence/verify_quotes.py            đối chiếu số bài, ngày, trích dẫn nguyên văn
    python evidence/verify_quotes.py --phieu    thêm phiếu kiểm tay nhãn (mọi bài có nhãn + 20 bài không nhãn, seed 42)

Phiếu: evidence/voz-kiem-tay.csv (điền cột nguoi_cham: 1 = bài nêu ít nhất một lỗi, 0 = không; không xem bảng nhãn).
Chữ của bài viết để ở evidence/raw-voz-doc.txt cho người chấm đọc, file này không được commit.
So khớp sau khi điền: python evidence/verify_quotes.py --so
"""
import csv
import html
import os
import random
import re
import sys
import unicodedata
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
LABELS = ["L1_thong_tin", "L2_trai_tuyen", "L3_dong_cua", "L4_chi_phi"]
SHEET = os.path.join(HERE, "voz-kiem-tay.csv")


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def norm(text):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text)).strip().lower()


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def parse(page):
    """Trang diễn đàn → {số bài: (ngày, link bài, chữ không gồm phần trích của người khác)}."""
    posts = {}
    for block in re.split(r'<article class="message message--post', page)[1:]:
        number = re.search(r">\s*#([\d,]+)\s*</a>", block)
        date = re.search(r'datetime="(\d{4}-\d\d-\d\d)', block)
        pid = re.search(r'data-content="post-(\d+)"', block)
        body = re.search(r'<div class="bbWrapper">(.*?)</div>\s*(?:<div class="js-selectToQuoteEnd">|</article>)', block, re.S)
        if not number:
            continue
        text = re.sub(r"<blockquote.*?</blockquote>", " [trích] ", body.group(1) if body else "", flags=re.S)
        text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", text))).strip()
        posts[number.group(1)] = (date.group(1) if date else "", pid.group(1) if pid else "", text)
    return posts


def verify(make_sheet):
    rows = read_csv(os.path.join(HERE, "voz-labels.csv"))
    pages = {}
    for url in sorted({r["url"] for r in rows}):
        pages[url] = parse(fetch(url))
        print("tải %-90s %d bài" % (url, len(pages[url])))
    found = [r for r in rows if r["post"] in pages[r["url"]]]
    same_date = [r for r in found if pages[r["url"]][r["post"]][0] == r["post_date"]]
    print("Bài trong bảng nhãn còn trên trang: %d/%d · đúng ngày: %d/%d" % (len(found), len(rows), len(same_date), len(found)))
    quoted = [r for r in found if r["trich"].strip()]
    ok = [r for r in quoted if norm(r["trich"]) in norm(pages[r["url"]][r["post"]][2])]
    print("Trích trong bảng nhãn khớp nguyên văn: %d/%d" % (len(ok), len(quoted)))
    with open(os.path.join(HERE, "summary.md"), encoding="utf-8") as f:
        cites = re.findall(r'^\d+\. "(.+)" \(VOZ (\d+) #(\d+)\)', f.read(), re.M)
    by_thread = {r["thread_id"]: r["url"] for r in rows}
    good = sum(norm(q) in norm(pages[by_thread[t]].get(n, ("", "", ""))[2]) for q, t, n in cites)
    print("Trích trong summary.md khớp nguyên văn: %d/%d" % (good, len(cites)))
    if make_sheet:
        if os.path.exists(SHEET):
            print("Đã có %s, không ghi đè." % SHEET)
        else:
            positive = [r for r in found if any(r[k] == "1" for k in LABELS)]
            rng = random.Random(42)
            negative = rng.sample([r for r in found if r not in positive], 20)
            sample = positive + negative
            rng.shuffle(sample)
            doc = []
            with open(SHEET, "w", encoding="utf-8-sig", newline="") as f:
                w = csv.writer(f)
                w.writerow(["stt", "thread_id", "post", "link", "nguoi_cham", "ghi_chu"])
                for i, r in enumerate(sample, 1):
                    _, pid, text = pages[r["url"]][r["post"]]
                    link = r["url"] + ("post-" + pid if pid else "")
                    w.writerow([i, r["thread_id"], r["post"], link, "", ""])
                    doc.append("== %d · thread %s · bài #%s\n%s\n%s\n" % (i, r["thread_id"], r["post"], link, text))
            with open(os.path.join(HERE, "raw-voz-doc.txt"), "w", encoding="utf-8") as f:
                f.write("\n".join(doc))
            print("Phiếu %d bài: %s · chữ để đọc: evidence/raw-voz-doc.txt" % (len(sample), SHEET))
    return 0 if len(ok) == len(quoted) and good == len(cites) else 1


def compare():
    labels = {(r["thread_id"], r["post"]): "1" if any(r[k] == "1" for k in LABELS) else "0"
              for r in read_csv(os.path.join(HERE, "voz-labels.csv"))}
    sheet = read_csv(SHEET)
    done = [r for r in sheet if r["nguoi_cham"].strip() in ("0", "1")]
    if not done:
        print("Phiếu chưa điền cột nguoi_cham.")
        return 1
    diff = [r for r in done if labels[(r["thread_id"], r["post"])] != r["nguoi_cham"].strip()]
    print("Đã chấm %d/%d bài · khớp nhãn %d/%d" % (len(done), len(sheet), len(done) - len(diff), len(done)))
    for r in diff:
        print("  lệch: thread %s #%s · người %s · bảng %s" % (r["thread_id"], r["post"], r["nguoi_cham"],
                                                            labels[(r["thread_id"], r["post"])]))
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    sys.exit(compare() if "--so" in sys.argv else verify("--phieu" in sys.argv))
