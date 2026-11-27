"""Công cụ của bài toán: tra dữ liệu Hà Nội, tính tiền, kiểm lịch. Tất cả CHỈ ĐỌC, không tác động ra ngoài.

Dữ liệu: data/hanoi_travel_kb.json (xem data/DATA_CARD.md).
Các hằng số có chữ "tự ước tính" KHÔNG có nguồn, output phải ghi rõ.
"""
import itertools
import json
import math
import os

from tracing import tool, TOOLS  # noqa: F401

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(_ROOT, "data", "hanoi_travel_kb.json"), encoding="utf-8") as _f:
    _KB = json.load(_f)

PLACES = {p["id"]: p for p in _KB["places"]}
TRANSFERS = _KB["airport_transfers"]
DATA_DATE = "27/11/2026"

DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
DAY_VI = dict(zip(DAYS, ["thứ Hai", "thứ Ba", "thứ Tư", "thứ Năm", "thứ Sáu", "thứ Bảy", "Chủ nhật"]))

# ---- Giả định của nhóm (tự ước tính, chốt tại CP2) ----
DU_PHONG = 0.10  # dự phòng 10% trên tổng các khoản
CUM = {
    "hoan_kiem_old_quarter": "A", "hai_ba_trung": "A", "long_bien": "A",
    "ba_dinh": "B", "dong_da": "B", "tay_ho": "B",
    "cau_giay": "C", "nam_tu_liem": "C",
    "gia_lam_bat_trang": "D", "son_tay": "E",
}
# Đi lại: đơn giá Grab Hà Nội (city_transport) và quãng đường lái xe OSRM (data/road_distances.json).
GIA_XE = _KB["city_transport"]
with open(os.path.join(_ROOT, "data", "road_distances.json"), encoding="utf-8") as _f:
    _ROAD = json.load(_f)
_IDX = {k: i for i, k in enumerate(_ROAD["ids"])}
DI_BO_TOI_DA_KM = 0.8    # gần hơn mức này thì đi bộ (tự ước tính)
# buổi: (bắt đầu, kết thúc) tính bằng phút
BUA = {"an_sang": (390, 510), "an_trua": (660, 810), "an_toi": (1050, 1200)}
BUOI = {"sang": (480, 720), "chieu": (780, 1080), "toi": (1140, 1350)}
THU_TU = ["an_sang", "sang", "an_trua", "chieu", "an_toi", "toi"]
TAG_KHONG_PHAI_BUA = {"trang_mieng", "ca_phe_trung"}


def _phut(s):
    h, m = s.split(":")
    return int(h) * 60 + int(m)


def hhmm(m):
    return "%02d:%02d" % (m // 60, m % 60)


def intervals(place_id, thu):
    v = PLACES[place_id]["opening_hours_by_day"].get(thu, "closed")
    if v == "closed":
        return []
    return [tuple(_phut(x) for x in iv.split("-")) for iv in v]


def la_mon_chinh(p):
    return p["category"] == "food" and not (TAG_KHONG_PHAI_BUA & set(p["tags"]))


def _slot(place_id, thu, earliest, window_end, meal):
    """Giờ bắt đầu sớm nhất hợp lệ, hoặc None. Tham quan phải kết thúc trong buổi; bữa ăn chỉ cần bắt đầu trong khung."""
    dur = PLACES[place_id]["suggested_duration_min"]
    for a, b in intervals(place_id, thu):
        start = max(earliest, a)
        if start + dur <= b and (start <= window_end if meal else start + dur <= window_end):
            return start
    return None


def nha(khu):
    """Mã điểm xuất phát đại diện cho một khu ở."""
    key = "KHU:%s" % khu
    return key if key in _IDX else "KHU:hoan_kiem_old_quarter"


def chang(a, b, so_nguoi):
    """Một chặng giữa hai mã (điểm hoặc KHU:...): km, phút, tiền, mã phương tiện. 1 người xe máy, từ 2 người ô tô."""
    km = round(_ROAD["km"][_IDX[a]][_IDX[b]], 1)
    if km <= DI_BO_TOI_DA_KM:
        return {"km": km, "phut": math.ceil(km / 4.5 * 60), "tien": 0, "ma": "DI-BO"}
    speed = 20 if km <= 10 else 30
    ma = "GRAB-BIKE" if so_nguoi == 1 else "GRAB-CAR4"
    g = GIA_XE[ma]
    xa = max(0.0, km - 2)
    mot_xe = g["first_2km_vnd"] + xa * g["per_km_vnd"] + xa / speed * 60 * g["per_min_vnd"]
    tien = int(math.ceil(mot_xe / 1000) * 1000) * math.ceil(so_nguoi / g["seats"])
    return {"km": km, "phut": math.ceil(km / speed * 60) + 5, "tien": tien, "ma": ma}


def san_bay_re_nhat(khu, so_nguoi):
    """Phương án Nội Bài rẻ nhất phục vụ khu ở (tính theo mức giá cao của khoảng)."""
    def cost(t):
        units = so_nguoi if t["fare_unit"] == "per_person" else math.ceil(so_nguoi / (7 if "7seat" in t["mode"] else 4))
        return t["fare_max_vnd"] * units
    pool = [t for t in TRANSFERS if khu in t["target_zones"]] or [t for t in TRANSFERS if t["fare_unit"] != "per_person"]
    best = min(pool, key=cost)
    return best, cost(best)


def xep_gio(lich, rb):
    """Xếp giờ theo thứ tự model chọn, kiểm vi phạm, tính các khoản chi. Hàm thường, không ghi trace."""
    errors, days_out, chi = [], [], {"an_uong": 0, "ve": 0, "di_chuyen": 0, "san_bay": 0}
    n, khu_o = rb["so_nguoi"], rb["khu_o"]
    plan = lich.get("ngay") if isinstance(lich, dict) else None
    if not isinstance(plan, list) or len(plan) != rb["so_ngay"]:
        return {"vi_pham": ["sai_so_ngay: lịch phải có đúng %d ngày" % rb["so_ngay"]], "ngay": [], "chi": chi,
                "du_phong": 0, "tong": 0}
    used = set()
    for i, day in enumerate(plan):
        thu = rb["thu"][i]
        cursor, pos, items = BUA["an_sang"][0], nha(khu_o), []
        meals_today = set()
        for slot in THU_TU:
            meal = slot in BUA
            raw = day.get(slot) if isinstance(day, dict) else None
            ids = ([raw] if raw else []) if meal else ([raw] if isinstance(raw, str) else list(raw or []))
            if meal and not ids:
                errors.append("thieu_bua: ngày %d thiếu %s" % (i + 1, slot))
                continue
            lo, hi = BUA[slot] if meal else BUOI[slot]
            cums = set()
            for pid in ids:
                p = PLACES.get(pid) if isinstance(pid, str) else None
                if not p:
                    errors.append("khong_co_du_lieu: %s không có trong dữ liệu" % pid)
                    continue
                if meal != (p["category"] == "food") or (meal and not la_mon_chinh(p)):
                    errors.append("sai_loai: %s không dùng được cho ô %s" % (pid, slot))
                    continue
                if meal:
                    if pid in meals_today:
                        errors.append("lap_quan: %s bị ăn hai bữa trong ngày %d" % (pid, i + 1))
                    meals_today.add(pid)
                if not meal:
                    if pid in used:
                        errors.append("trung_diem: %s bị xếp hai lần" % pid)
                    used.add(pid)
                    cums.add(CUM.get(p["zone"]))
                if not intervals(pid, thu):
                    errors.append("dong_cua: %s (%s) đóng cửa %s" % (pid, p["name"], DAY_VI[thu]))
                    continue
                leg = chang(pos, pid, n)
                start = _slot(pid, thu, max(cursor + leg["phut"], lo), hi, meal)
                if start is None:
                    errors.append("ngoai_gio: %s (%s) không vừa giờ mở cửa trong ô %s ngày %d" % (pid, p["name"], slot, i + 1))
                    continue
                end = start + p["suggested_duration_min"]
                money = p["ticket_adult_vnd"] * n
                chi["di_chuyen"] += leg["tien"]
                chi["an_uong" if meal else "ve"] += money
                items.append({"o": slot, "id": pid, "ten": p["name"], "tu": hhmm(start), "den": hhmm(end),
                              "tien": money, "di": leg})
                cursor, pos = end, pid
            if len(cums) > 1:
                errors.append("trai_tuyen: ô %s ngày %d trộn các cụm quận %s" % (slot, i + 1, "/".join(sorted(map(str, cums)))))
        if not any(PLACES[m["id"]]["category"] == "attraction" for m in items):
            errors.append("ngay_trong: ngày %d chưa có điểm tham quan nào" % (i + 1))
        back = chang(pos, nha(khu_o), n)
        chi["di_chuyen"] += back["tien"]
        days_out.append({"thu": thu, "muc": items, "ve_noi_o": back})
    san_bay = None
    if rb.get("di_may_bay"):
        t, one_way = san_bay_re_nhat(khu_o, n)
        chi["san_bay"] = 2 * one_way
        san_bay = {"id": t["id"], "ten": t["name"], "mot_chieu": one_way, "gio_chay": t["operating_hours"]}
    base = sum(chi.values())
    du_phong = int(round(base * DU_PHONG))
    tong = base + du_phong
    if tong > rb["ngan_sach_vnd"]:
        errors.append("vuot_ngan_sach: tổng %d đ vượt trần %d đ" % (tong, rb["ngan_sach_vnd"]))
    return {"vi_pham": errors, "ngay": days_out, "chi": chi, "du_phong": du_phong, "tong": tong, "san_bay": san_bay}


@tool
def tra_dia_diem(thu_di: list, so_thich: list) -> dict:
    """tra_dia_diem · Input: danh sách thứ của chuyến đi (mon..sun), sở thích (list). Output: {"tham_quan": [...], "quan_an": [...]}
    chỉ gồm điểm mở ít nhất một ngày trong chuyến, kèm id, tên, khu, cụm, giờ theo ngày, giá. Không tác động ra ngoài."""
    out = {"tham_quan": [], "quan_an": []}
    want = set(so_thich or [])
    group = {"di_tich": {"di_tich", "lich_su", "bao_tang", "van_hoa"}, "am_thuc": {"am_thuc"},
             "chup_anh": {"chup_anh", "kien_truc"}, "mua_dac_san": {"mua_sam", "cho_dem", "lang_nghe"}}
    tags_wanted = set().union(*[group.get(w, {w}) for w in want]) if want else set()
    for pid, p in PLACES.items():
        gio = {d: [hhmm(a) + "-" + hhmm(b) for a, b in intervals(pid, d)] for d in thu_di}
        if not any(gio.values()):
            continue
        row = {"id": pid, "ten": p["name"], "khu": p["zone"], "cum": CUM.get(p["zone"]), "gio": gio,
               "gia": p["ticket_adult_vnd"], "phut": p["suggested_duration_min"]}
        if p["category"] == "food":
            if la_mon_chinh(p):
                out["quan_an"].append(row)
        else:
            row["hop_so_thich"] = bool(tags_wanted & set(p["tags"]))
            out["tham_quan"].append(row)
    return out


@tool
def loc_theo_o(rang_buoc: dict) -> dict:
    """loc_theo_o · Input: ràng buộc chuyến đi. Output: {"diem": {mã: mô tả ngắn}, "o_hop_le": [mỗi ngày: ô -> mã mở
    cửa kịp trong ô đó]}. Không tác động ra ngoài."""
    diem, ngay = {}, []
    home = nha(rang_buoc["khu_o"])
    for thu in rang_buoc["thu"]:
        o = {}
        for slot in THU_TU:
            meal = slot in BUA
            lo, hi = BUA[slot] if meal else BUOI[slot]
            ids = [pid for pid, p in PLACES.items()
                   if (la_mon_chinh(p) if meal else p["category"] == "attraction")
                   and _slot(pid, thu, lo, hi, meal) is not None]
            o[slot] = ids
            for pid in ids:
                p = PLACES[pid]
                diem[pid] = [p["name"], "cum " + CUM.get(p["zone"], "?"), p["ticket_adult_vnd"],
                             chang(home, pid, rang_buoc["so_nguoi"])["km"]] + ([] if meal else [",".join(p["tags"][:3])])
        ngay.append(dict({"thu": thu}, **o))
    return {"diem": diem, "o_hop_le": ngay}


@tool
def ha_chi_phi(lich: dict, rang_buoc: dict, o_hop_le: list) -> dict:
    """ha_chi_phi · Input: lịch chỉ còn lỗi vượt ngân sách. Output: {"lich", "doi": số ô đã đổi, "dat": bool}. Đổi dần
    từng ô (quán ăn, điểm không được yêu cầu) sang lựa chọn hợp lệ làm tổng giảm nhiều nhất. Không tác động ra ngoài."""
    plan = json.loads(json.dumps(lich))
    wanted = set(rang_buoc.get("diem_muon_di") or [])
    res = xep_gio(plan, rang_buoc)
    changes = 0
    while res["vi_pham"] and changes < 24:
        if any(not e.startswith("vuot_ngan_sach") for e in res["vi_pham"]):
            break
        best = None
        for i, day in enumerate(plan["ngay"]):
            for slot in THU_TU:
                meal = slot in BUA
                now = day.get(slot)
                if not now or (not meal and now[0] in wanted):
                    continue
                options = list(o_hop_le[i][slot]) + ([] if meal else [None])  # None: bỏ trống buổi tham quan
                for pid in options:
                    trial = json.loads(json.dumps(plan))
                    trial["ngay"][i][slot] = pid if meal else ([pid] if pid else [])
                    r = xep_gio(trial, rang_buoc)
                    if all(e.startswith("vuot_ngan_sach") for e in r["vi_pham"]) and r["tong"] < res["tong"] \
                            and (best is None or r["tong"] < best[1]["tong"]):
                        best = (trial, r)
        if best is None:
            break
        plan, res = best
        changes += 1
    return {"lich": plan, "doi": changes, "dat": not res["vi_pham"]}


@tool
def kiem_tra_mo_cua(diem_id: str, thu: str) -> dict:
    """kiem_tra_mo_cua · Input: mã điểm, thứ (mon..sun). Output: {co_du_lieu, mo_cua, gio, ghi_chu}. Không tác động ra ngoài."""
    p = PLACES.get(diem_id)
    if not p:
        return {"co_du_lieu": False, "mo_cua": False, "gio": [], "ghi_chu": ""}
    iv = intervals(diem_id, thu)
    return {"co_du_lieu": True, "mo_cua": bool(iv), "gio": [hhmm(a) + "-" + hhmm(b) for a, b in iv], "ghi_chu": p["notes"]}


@tool
def tra_di_chuyen_noi_bai(khu_o: str, so_nguoi: int) -> dict:
    """tra_di_chuyen_noi_bai · Input: khu ở, số người. Output: phương án rẻ nhất và giá một chiều. Không tác động ra ngoài."""
    t, cost = san_bay_re_nhat(khu_o, so_nguoi)
    return {"id": t["id"], "ten": t["name"], "mot_chieu": cost, "gio_chay": t["operating_hours"]}


@tool
def uoc_tinh_di_chuyen(khu_a: str, khu_b: str, so_nguoi: int) -> dict:
    """uoc_tinh_di_chuyen · Input: hai khu, số người. Output: {km, phut, tien, ma}; đơn giá Grab công bố, quãng đường
    OSRM giữa hai điểm đại diện khu. Không tác động ra ngoài."""
    return chang(nha(khu_a), nha(khu_b), so_nguoi)


@tool
def chi_phi_toi_thieu(rang_buoc: dict) -> int:
    """chi_phi_toi_thieu · Input: ràng buộc chuyến đi. Output: cận dưới (đồng) gồm 3 quán khác nhau rẻ nhất mỗi ngày,
    vé 0 đ, không tính đi lại, cộng Nội Bài nếu đi máy bay và dự phòng. Không tác động ra ngoài."""
    total = 0
    for thu in rang_buoc["thu"]:
        pools = []
        for slot, (lo, hi) in BUA.items():
            pool = sorted((p["ticket_adult_vnd"], pid) for pid, p in PLACES.items()
                          if la_mon_chinh(p) and _slot(pid, thu, lo, hi, True) is not None)
            pools.append(pool[:4])
        total += min(sum(c for c, _ in combo) for combo in itertools.product(*pools)
                     if len({i for _, i in combo}) == len(combo)) * rang_buoc["so_nguoi"]
    if rang_buoc.get("di_may_bay"):
        total += 2 * san_bay_re_nhat(rang_buoc["khu_o"], rang_buoc["so_nguoi"])[1]
    return int(round(total * (1 + DU_PHONG)))


@tool
def kiem_lich_trinh(lich: dict, rang_buoc: dict) -> dict:
    """kiem_lich_trinh · Input: lịch nháp (mã điểm theo ô), ràng buộc. Output: lịch đã xếp giờ, các khoản chi, tổng,
    danh sách vi phạm (đóng cửa, ngoài giờ, trùng, thiếu bữa, trái tuyến, vượt ngân sách). Không tác động ra ngoài."""
    return xep_gio(lich, rang_buoc)
