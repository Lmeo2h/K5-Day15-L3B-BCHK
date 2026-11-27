"""Lớp kiểm bằng code cho kết quả đọc yêu cầu của model (cải tiến sau lượt 1).

Model hay đọc sai ba thứ: nơi nào là ngoài phạm vi, câu nào đang hỏi đi lại từ sân bay, và địa điểm nào được
gọi tên. Ba thứ này kiểm được bằng luật trên chính tin nhắn, nên code đối chiếu và sửa lại.
"""
import re

import tools

# Điểm đến ngoài Hà Nội hay được hỏi. Tên đứng sau "từ", "ở", "dân", "người" là nơi xuất phát, không phải điểm đến.
NGOAI = (r"đà nẵng|hạ long|sa ?pa|huế|đà lạt|nha trang|phú quốc|hội an|ninh bình|tam đảo|hải phòng|cần thơ|vũng tàu|"
         r"quy nhơn|phan thiết|mũi né|hà giang|mộc châu|cát bà|bangkok|thái lan|singapore|nhật bản|hàn quốc")
DAT_HO = re.compile(r"đặt|thanh toán|mua (vé )?(hộ|giúp|dùm)")
SAN_BAY = re.compile(r"nội bài|noi bai|sân bay|\bnb\b")
DI_MAY_BAY = re.compile(r"nội bài|noi bai|sân bay|\bnb\b|máy bay|chuyến bay|\bbay (ra|đến|vào|từ)\b|vietjet|bamboo")
# Chỉ nhận nơi ở khi tin nhắn nói rõ "ở / nghỉ / khách sạn ... <khu>"; điểm muốn đến không phải nơi ở.
NOI_O = {"hoan_kiem_old_quarter": "phố cổ|hoàn kiếm|hồ gươm|bờ hồ", "ba_dinh": "ba đình", "dong_da": "đống đa|láng hạ",
         "tay_ho": "tây hồ|hồ tây", "cau_giay": "cầu giấy", "nam_tu_liem": "nam từ liêm|mỹ đình",
         "hai_ba_trung": "hai bà trưng", "long_bien": "long biên", "gia_lam_bat_trang": "bát tràng|gia lâm",
         "son_tay": "sơn tây|đường lâm"}


PHA_QUY_TAC = re.compile(r"bỏ qua|quản trị|\badmin\b|mọi giới hạn|vé[^.]{0,25}\b0 đồng")
SO_THICH = {"chup_anh": r"chụp", "di_tich": r"di tích|lịch sử|bảo tàng", "mua_dac_san": r"đặc sản|mua quà"}


def noi_o(text):
    t = text.lower()
    for zone, names in NOI_O.items():
        if re.search(r"\b(ở|nghỉ|ngủ|khách sạn|ks|homestay|trọ)\s+(tại\s+|khu\s+|quận\s+|gần\s+|trong\s+)*(%s)" % names, t):
            return zone
    return None
DI_LAI = re.compile(r"taxi|grab|xe (buýt|bus)|\bbus\b|xe công nghệ|đi bằng gì|thuê xe|vào (ks|khách sạn)|"
                    r"về (ks|khách sạn|trung tâm|nội thành)")
CHUNG_CHUNG = {"bảo tàng", "hà nội", "việt nam", "lịch sử", "quốc gia", "phố cổ", "chợ đêm", "đi bộ", "công viên",
               "di tích", "nhà hát", "không gian", "hoàn kiếm", "tây hồ", "hồ tây", "làng cổ", "phụ cận", "cơ sở"}
TEN_GOI_KHAC = {"HN-ATTR-01": ["lăng bác", "lăng chủ tịch"]}


def duoc_nhac(pid, text):
    """Địa điểm có được gọi tên trong tin nhắn không: trùng một cặp từ riêng của tên (bỏ phần trong ngoặc)."""
    t = " " + " ".join(re.findall(r"\w+", text.lower())) + " "
    if any(" %s " % a in t for a in TEN_GOI_KHAC.get(pid, [])):
        return True
    words = re.findall(r"\w+", re.sub(r"\(.*?\)", " ", tools.PLACES[pid]["name"]).lower())
    grams = (" ".join(words[i:i + 2]) for i in range(len(words) - 1))
    return any(g not in CHUNG_CHUNG and " %s " % g in t for g in grams)


def diem_ngoai_ha_noi(text):
    t = text.lower()
    for m in re.finditer(NGOAI, t):
        before = t[max(0, m.start() - 12):m.start()]
        if not re.search(r"(từ|ở|dân|người)\s+(tp\.?\s*)?$", before):
            return m.group()
    return None


def gio_hoi(text):
    """Giờ được nhắc trong câu hỏi đi lại, đổi ra phút trong ngày; None nếu không nhắc."""
    m = re.search(r"\b(\d{1,2})\s*(?:h|giờ)\s*(\d{2})?\s*(đêm|khuya|sáng|chiều|tối)?", text.lower())
    if not m:
        return None
    hour, minute, part = int(m.group(1)), int(m.group(2) or 0), m.group(3)
    if hour == 12 and part in ("đêm", "khuya"):
        hour = 0
    elif part in ("chiều", "tối") and hour < 12:
        hour += 12
    elif part in ("đêm", "khuya") and 8 <= hour < 12:
        hour += 12
    return (hour % 24) * 60 + minute


def sua(r, text):
    """Trả về bản đã sửa của r (dict ràng buộc từ model)."""
    t = text.lower()
    oos = {x for x in r.get("ngoai_pham_vi") or [] if x != "ngoai_ha_noi"}
    if not DAT_HO.search(t):
        oos -= {"dat_ve", "thanh_toan"}
    outside = diem_ngoai_ha_noi(text)
    if outside:
        oos.add("ngoai_ha_noi")
        r["co_phan_ha_noi"] = bool(re.search(r"hà nội|\bhn\b", t))
    elif not oos:
        r["co_phan_ha_noi"] = True
    r["ngoai_pham_vi"] = sorted(oos)

    r["di_may_bay"] = bool(DI_MAY_BAY.search(t))
    if PHA_QUY_TAC.search(t):
        r["yeu_cau_pha_quy_tac"] = True
    said = [k for k, pat in SO_THICH.items() if re.search(pat, t)]
    r["so_thich"] = list(dict.fromkeys(list(r.get("so_thich") or []) + said))
    r["khu_o"] = noi_o(text)
    planning = r.get("so_ngay") or r.get("ngan_sach_vnd")
    r["hoi_di_lai"] = bool(DI_LAI.search(t) and not planning and not outside)
    if r["hoi_di_lai"]:
        r["loai"] = "hoi_thong_tin"

    named = [pid for pid, p in tools.PLACES.items() if p["category"] == "attraction" and duoc_nhac(pid, text)]
    kept = [pid for pid in r.get("diem_muon_di") or [] if pid in tools.PLACES and duoc_nhac(pid, text)]
    r["diem_muon_di"] = list(dict.fromkeys(kept + named))
    return r
