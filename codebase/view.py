"""Chuyển kết quả của answer() thành dữ liệu để giao diện vẽ. Chỉ đọc, không gọi model, không đổi số liệu.

Mọi giờ, giá, quãng đường lấy nguyên từ kết quả của tools.py và data/hanoi_travel_kb.json.
"""
from urllib.parse import urlencode

import tools

KHU = {"hoan_kiem_old_quarter": "Phố cổ, Hoàn Kiếm", "ba_dinh": "Ba Đình", "dong_da": "Đống Đa", "tay_ho": "Tây Hồ",
       "cau_giay": "Cầu Giấy", "nam_tu_liem": "Nam Từ Liêm", "hai_ba_trung": "Hai Bà Trưng", "long_bien": "Long Biên",
       "gia_lam_bat_trang": "Bát Tràng, Gia Lâm", "son_tay": "Sơn Tây"}
SO_THICH = {"di_tich": "Di tích", "am_thuc": "Ẩm thực", "chup_anh": "Chụp ảnh", "mua_dac_san": "Mua đặc sản"}
BUOI = {"an_sang": "Ăn sáng", "sang": "Buổi sáng", "an_trua": "Ăn trưa", "chieu": "Buổi chiều", "an_toi": "Ăn tối",
        "toi": "Buổi tối"}
PHUONG_TIEN = {"DI-BO": "Đi bộ", "GRAB-BIKE": "GrabBike", "GRAB-CAR4": "GrabCar 4 chỗ"}
# trường "verification" trong dữ liệu → (mức, nhãn hiển thị). Mức: ok · mot_phan · chua
KIEM = {
    "chinh_thuc": ("ok", "Nguồn chính thức"),
    "chinh_thuc_gio": ("mot_phan", "Giờ theo nguồn chính thức, giá chưa kiểm"),
    "chinh_thuc_khong_ngay": ("mot_phan", "Trang chính thức, không ghi ngày"),
    "bao_chi": ("mot_phan", "Theo báo chí"),
    "thu_cap": ("mot_phan", "Nguồn thứ cấp"),
    "nguon_phu_chua_doc_trang": ("chua", "Nguồn phụ, chưa đọc trang"),
    "mau_thuan": ("chua", "Các nguồn mâu thuẫn"),
}
CHUA_KIEM = ("chua", "Chưa kiểm nguồn")

_ROAD_POINT = dict(zip(tools._ROAD["ids"], tools._ROAD["points"]))


def _kiem(record):
    level, label = KIEM.get(record.get("verification"), CHUA_KIEM)
    return {"muc": level, "nhan": label}


def _nguon(record):
    url = str(record.get("source_url") or "")
    if not url.startswith(("https://", "http://")):
        return None
    return {"ten": record.get("source_name") or "Nguồn", "url": url}


def _toa_do(key):
    point = _ROAD_POINT.get(key)
    return {"lat": point[0], "lng": point[1]} if point else None


def diem(pid):
    p = tools.PLACES[pid]
    lat, lng = p.get("approx_lat"), p.get("approx_lng")
    query = "%s, %s" % (p["name"], p.get("address") or "Hà Nội")
    return {"id": pid, "ten": p["name"], "loai": p["category"], "quan": p.get("district"), "dia_chi": p.get("address"),
            "toa_do": {"lat": lat, "lng": lng} if lat is not None and lng is not None else None,
            "ban_do": "https://www.google.com/maps/search/?" + urlencode({"api": 1, "query": query}),
            "kiem": _kiem(p), "nguon": _nguon(p), "luu_y": p.get("notes") or ""}


def _tuyen_google(home, stops):
    """Link chỉ đường cả ngày theo Google Maps URLs: đi từ khu ở, qua các điểm, quay về."""
    if not home or not stops:
        return None
    here = "%.6f,%.6f" % (home["lat"], home["lng"])
    params = {"api": 1, "origin": here, "destination": here, "travelmode": "driving",
              "waypoints": "|".join("%.6f,%.6f" % (s["lat"], s["lng"]) for s in stops)}
    return "https://www.google.com/maps/dir/?" + urlencode(params)


def _chang(leg):
    return {"km": leg["km"], "phut": leg["phut"], "tien": leg["tien"], "ma": leg["ma"],
            "ten": PHUONG_TIEN.get(leg["ma"], leg["ma"])}


def lich(d):
    rb, res, reasons = d["rang_buoc"], d["lich"], d.get("ly_do") or {}
    home = _toa_do(tools.nha(rb["khu_o"]))
    days = []
    for number, day in enumerate(res["ngay"], 1):
        items, stops = [], []
        for m in day["muc"]:
            place = diem(m["id"])
            why = reasons.get(m["id"]) if place["loai"] == "attraction" and isinstance(reasons, dict) else None
            items.append({"o": m["o"], "buoi": BUOI.get(m["o"], m["o"]), "tu": m["tu"], "den": m["den"],
                          "tien": m["tien"], "di": _chang(m["di"]), "ly_do": str(why) if why else "", "diem": place})
            if place["toa_do"]:
                stops.append(place["toa_do"])
        back = _chang(day["ve_noi_o"])
        total = sum(i["tien"] + i["di"]["tien"] for i in items) + back["tien"]
        days.append({"so": number, "thu": tools.DAY_VI[day["thu"]], "muc": items, "ve": back, "tong": total,
                     "tuyen": _tuyen_google(home, stops)})
    c = res["chi"]
    costs = [("an_uong", "Ăn uống", c["an_uong"]), ("ve", "Vé tham quan", c["ve"]),
             ("di_chuyen", "Đi lại trong thành phố", c["di_chuyen"]), ("san_bay", "Nội Bài khứ hồi", c["san_bay"]),
             ("du_phong", "Dự phòng 10%", res["du_phong"])]
    airport = None
    if res.get("san_bay"):
        s = res["san_bay"]
        airport = {"id": s["id"], "ten": s["ten"], "mot_chieu": s["mot_chieu"], "gio_chay": s["gio_chay"]}
    return {"so_ngay": rb["so_ngay"], "so_nguoi": rb["so_nguoi"], "khu": KHU.get(rb["khu_o"], rb["khu_o"]),
            "nha": home, "ngay": days, "chi": [{"khoa": k, "nhan": n, "tien": v} for k, n, v in costs],
            "tong": res["tong"], "tran": rb["ngan_sach_vnd"], "san_bay": airport,
            "nguon_di_lai": {"ten": tools.GIA_XE["source_name"], "url": tools.GIA_XE.get("source_url")}}


def thong_tin(d):
    by_id = {t["id"]: t for t in tools.TRANSFERS}
    trips = []
    for tid in d.get("chuyen") or []:
        t = by_id[tid]
        trips.append({"id": tid, "ten": t["name"], "tuyen": t.get("route_summary") or "", "gio": t["operating_hours"],
                      "gia_min": t["fare_min_vnd"], "gia_max": t["fare_max_vnd"],
                      "don_vi": "người" if t["fare_unit"] == "per_person" else "xe",
                      "kiem": _kiem(t), "nguon": _nguon(t)})
    places = []
    for pid in d.get("diem") or []:
        p = tools.PLACES[pid]
        closed = [tools.DAY_VI[x] for x in tools.DAYS if not tools.intervals(pid, x)]
        places.append(dict(diem(pid), gio=p["opening_hours_summary"], ngay_dong=closed, gia=p["price_note"]))
    return {"chuyen": trips, "diem": places, "khong_co": d.get("khong_co") or [], "canh_bao": d.get("canh_bao") or []}


def _rang_buoc(rb):
    """Ràng buộc đã đọc, để giao diện soạn lại câu khi người dùng bấm gợi ý."""
    return {"so_ngay": rb["so_ngay"], "so_nguoi": rb["so_nguoi"], "ngan_sach": rb["ngan_sach_vnd"],
            "thu": tools.DAY_VI[rb["thu"][0]], "khu": rb["khu_o"], "khu_ten": KHU.get(rb["khu_o"], rb["khu_o"]),
            "so_thich": rb.get("so_thich") or [], "di_may_bay": bool(rb.get("di_may_bay")),
            "diem_muon_di": [tools.PLACES[p]["name"] for p in rb.get("diem_muon_di") or [] if p in tools.PLACES]}


def build(result):
    kind, d = result.get("loai"), result.get("du_lieu") or {}
    out = {"ghi_chu": d.get("ghi_chu") or []}
    if kind == "lich":
        out.update(lich(d))
    elif kind == "thong_tin":
        out.update(thong_tin(d))
    elif kind == "hoi_lai":
        out.update(thieu=d.get("thieu") or [], qua_so_ngay=bool(d.get("qua_so_ngay")))
    elif kind == "khong_du_tien":
        out.update(toi_thieu=d["toi_thieu"], rang_buoc=_rang_buoc(d["rang_buoc"]))
    elif kind == "khong_xep_duoc":
        out.update(vuong=d.get("vuong") or [], rang_buoc=_rang_buoc(d["rang_buoc"]))
    return out
