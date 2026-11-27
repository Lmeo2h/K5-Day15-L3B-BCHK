"""AI GIẢ cho CP2: thay hai lời gọi model để luồng chạy hết khi chưa có API key.

Đây là regex và thuật toán tham lam viết chung chung, KHÔNG phải giải pháp và không được tính vào kết quả đánh giá.
"""
import re

import tools

_DAYS = {"hai": "mon", "2": "mon", "ba": "tue", "3": "tue", "tư": "wed", "4": "wed", "năm": "thu", "5": "thu",
         "sáu": "fri", "6": "fri", "bảy": "sat", "7": "sat"}
_ALIAS = {"lăng bác": "HN-ATTR-01", "văn miếu": "HN-ATTR-02", "hoàng thành": "HN-ATTR-03", "hỏa lò": "HN-ATTR-04",
          "dân tộc học": "HN-ATTR-05", "quân sự": "HN-ATTR-06", "bát tràng": "HN-ATTR-20", "đồng xuân": "HN-ATTR-26"}


def _budget(t):
    m = re.search(r"(\d+)\s*(?:triệu|tr)\s*(\d)\b", t)
    if m:
        return int(m.group(1)) * 1000000 + int(m.group(2)) * 100000
    m = re.search(r"(\d+(?:[.,]\d+)?)\s*(?:triệu|tr\b|củ)", t)
    if m:
        return int(float(m.group(1).replace(",", ".")) * 1000000)
    m = re.search(r"(\d+)\s*(?:k\b|nghìn|ngàn)", t)
    if m:
        return int(m.group(1)) * 1000
    m = re.search(r"(\d{1,3}(?:[.,]\d{3})+)", t)
    return int(re.sub(r"[.,]", "", m.group(1))) if m else None


def trich(text):
    t = text.lower()
    days = re.search(r"(\d+)\s*ngày", t)
    people = re.search(r"(\d+)\s*người", t)
    date = re.search(r"\b(\d{1,2})/(\d{1,2})(?:/(\d{4}))?\b", t)
    thu = "sun" if "chủ nhật" in t else None
    m = re.search(r"thứ\s*(hai|ba|tư|năm|sáu|bảy|[2-7])", t)
    if m:
        thu = _DAYS[m.group(1)]
    other = re.search(r"đà nẵng|sa ?pa|hạ long|đà lạt|nha trang|phú quốc|\bhuế\b", t)
    oos = (["ngoai_ha_noi"] if other else []) + (["dat_ve"] if re.search(r"đặt (vé|phòng)|mua vé giúp", t) else []) \
        + (["thanh_toan"] if "thanh toán" in t else [])
    likes = [k for k, pat in (("di_tich", "di tích|lịch sử|bảo tàng"), ("am_thuc", "ăn"),
                              ("chup_anh", "chụp"), ("mua_dac_san", "đặc sản|mua")) if re.search(pat, t)]
    wanted = [pid for name, pid in _ALIAS.items() if name in t]
    asking = bool(re.search(r"giá[^.?]{0,40}(bao nhiêu|nhiêu)|mấy giờ|có mở cửa|xe (buýt|bus) nào", t)) and not days
    return {
        "loai": "hoi_thong_tin" if asking else "lap_lich",
        "so_ngay": int(days.group(1)) if days else None,
        "ngay_bat_dau": "%s-%02d-%02d" % (date.group(3) or "2026", int(date.group(2)), int(date.group(1))) if date else None,
        "thu_bat_dau": thu,
        "ngan_sach_vnd": _budget(t),
        "so_nguoi": int(people.group(1)) if people else (None if "nhóm" in t else 1),
        "khu_o": "hoan_kiem_old_quarter" if re.search(r"phố cổ|hoàn kiếm", t) else None,
        "so_thich": likes,
        "diem_muon_di": wanted,
        "diem_khong_co": [],
        "di_may_bay": bool(re.search(r"nội bài|sân bay|máy bay", t)),
        "ngoai_pham_vi": oos,
        "co_phan_ha_noi": not other or "hà nội" in t,
        "yeu_cau_pha_quy_tac": bool(re.search(r"bỏ qua|quản trị|admin|0 đồng", t)),
    }


def xep(candidates, rb):
    """Xếp tham lam: mỗi ô thử lần lượt ứng viên, giữ cái đầu tiên không gây vi phạm."""
    home = tools.nha(rb["khu_o"])

    def meal_cost(c):
        return c["gia"] + 2 * tools.chang(home, c["id"], 1)["tien"]

    meals = sorted(candidates["quan_an"], key=meal_cost)
    sights = sorted(candidates["tham_quan"], key=lambda c: (c["id"] not in rb.get("diem_muon_di", []),
                                                             not c["hop_so_thich"], c["gia"]))
    plan = {"ngay": [{} for _ in range(rb["so_ngay"])]}

    def clean():
        errs = tools.xep_gio(plan, rb)["vi_pham"]
        return not [e for e in errs if not e.startswith("thieu_bua")]

    for i, day in enumerate(plan["ngay"]):
        for slot in tools.BUA:
            for c in meals[i % 3:] + meals[:i % 3]:
                day[slot] = c["id"]
                if clean():
                    break
                del day[slot]
    used = set()
    for day in plan["ngay"]:
        for slot in ("sang", "chieu"):
            for c in sights:
                if c["id"] in used:
                    continue
                day[slot] = [c["id"]]
                if clean():
                    used.add(c["id"])
                    break
                del day[slot]
    return plan
