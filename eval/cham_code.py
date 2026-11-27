"""Chấm hai metric code (lich_hop_le, ngan_sach_dung) trên một file lượt chạy. KHÔNG sửa file lượt.

    python eval/cham_code.py eval/run-1.csv

Đọc lại phần chữ của output, đối chiếu data/hanoi_travel_kb.json và ràng buộc của từng câu ở eval/rang_buoc.csv.
Không dùng kết quả của bộ kiểm trong codebase/: ràng buộc, quãng đường và tiền được tính lại ở đây.
"""
import csv
import json
import math
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(ROOT, "data", "hanoi_travel_kb.json"), encoding="utf-8") as f:
    KB = json.load(f)
PLACES = {p["id"]: p for p in KB["places"]}
with open(os.path.join(ROOT, "data", "road_distances.json"), encoding="utf-8") as f:
    ROAD = json.load(f)
with open(os.path.join(ROOT, "eval", "rang_buoc.csv"), encoding="utf-8-sig", newline="") as f:
    RB = {r["id"]: r for r in csv.DictReader(f)}
DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
THU = dict(zip(["thứ Hai", "thứ Ba", "thứ Tư", "thứ Năm", "thứ Sáu", "thứ Bảy", "Chủ nhật"], DAYS))
ITEM = re.compile(r"^\s+(\d\d:\d\d)-(\d\d:\d\d) (Ăn sáng|Ăn trưa|Ăn tối|Sáng|Chiều|Tối): .*?\[(HN-[A-Z]+-\d+)\] ([\d.]+) đ")
LEG = re.compile(r"^\s+(đi lại|về nơi ở) ([\d.]+) km \[(DI-BO|GRAB-BIKE|GRAB-CAR4)\] ([\d.]+) đ")


def num(s):
    return int(s.replace(".", ""))


def mins(s):
    h, m = s.split(":")
    return int(h) * 60 + int(m)


def centre(zone):
    return "KHU:%s" % zone


def leg(a, b, people):
    """(km, phút, tiền, mã). Công thức và hằng số ghi ở spec.md §4."""
    km = round(ROAD["km"][ROAD["ids"].index(a)][ROAD["ids"].index(b)], 1)
    if km <= 0.8:
        return km, math.ceil(km / 4.5 * 60), 0, "DI-BO"
    speed = 20 if km <= 10 else 30
    code = "GRAB-BIKE" if people == 1 else "GRAB-CAR4"
    g = KB["city_transport"][code]
    far = max(0.0, km - 2)
    one = g["first_2km_vnd"] + far * g["per_km_vnd"] + far / speed * 60 * g["per_min_vnd"]
    return km, math.ceil(km / speed * 60) + 5, int(math.ceil(one / 1000) * 1000) * math.ceil(people / g["seats"]), code


def airport(zone, people):
    def cost(t):
        units = people if t["fare_unit"] == "per_person" else math.ceil(people / (7 if "7seat" in t["mode"] else 4))
        return t["fare_max_vnd"] * units
    all_t = KB["airport_transfers"]
    pool = [t for t in all_t if zone in t["target_zones"]] or [t for t in all_t if t["fare_unit"] != "per_person"]
    return min(cost(t) for t in pool)


def check(case_id, output):
    """→ None nếu output không có lịch; (lỗi lịch, lỗi tiền) nếu có."""
    head = re.search(r"LỊCH (\d+) NGÀY cho (\d+) người, trần ([\d.]+) đ", output)
    if not head:
        return None
    rb = RB.get(case_id)
    if not rb or rb["co_lich"] == "khong":
        return ["xuất lịch cho câu không được xuất lịch"], []
    n_days, people, cap = int(rb["so_ngay"]), int(rb["so_nguoi"]), int(rb["tran_vnd"])
    home = centre(rb["khu_o"])
    lich, budget = [], []
    if int(head.group(1)) != n_days or int(head.group(2)) != people:
        lich.append("số ngày hoặc số người khác ràng buộc")
    start = DAYS.index(rb["thu_bat_dau"])
    tien = {"an_uong": 0, "ve": 0, "di": 0}
    day, index, pos, last, pending, meals, returned, sights = None, 0, home, 0, None, [], True, 0

    def close_day():
        if day is not None:
            if sights == 0:
                lich.append("ngày %d không có điểm tham quan" % index)
            if len(meals) != 3 or len(set(meals)) != 3:
                lich.append("ngày %d không đủ 3 bữa ở 3 quán khác nhau" % index)
            if not returned:
                budget.append("ngày %d thiếu chặng về nơi ở" % index)

    for line in output.splitlines():
        m = re.match(r"^Ngày \d+ \((.+)\)", line)
        if m:
            close_day()
            day = THU.get(m.group(1))
            if day != DAYS[(start + index) % 7]:
                lich.append("ngày %d sai thứ" % (index + 1))
            index += 1
            pos, last, pending, meals, returned, sights = home, 0, None, [], False, 0
            continue
        m = LEG.match(line)
        if m:
            printed = (float(m.group(2)), m.group(3), num(m.group(4)))
            tien["di"] += printed[2]
            if m.group(1) == "về nơi ở":
                km, _, cost, code = leg(pos, home, people)
                if printed != (km, code, cost):
                    budget.append("chặng về ngày %d sai" % index)
                returned = True
            else:
                pending = printed
            continue
        m = ITEM.match(line)
        if not m:
            continue
        a, b, slot, pid, money = mins(m.group(1)), mins(m.group(2)), m.group(3), m.group(4), num(m.group(5))
        p = PLACES.get(pid)
        if not p or day is None:
            lich.append("mã lạ %s" % pid)
            continue
        km, travel, cost, code = leg(pos, pid, people)
        if pending != (km, code, cost):
            budget.append("chặng đến %s sai hoặc thiếu" % pid)
        hours = p["opening_hours_by_day"].get(day, "closed")
        meal = slot.startswith("Ăn")
        if hours == "closed":
            lich.append("%s đóng cửa %s" % (pid, day))
        elif not any(mins(x.split("-")[0]) <= a and b <= mins(x.split("-")[1]) for x in hours):
            lich.append("%s ngoài giờ %s %s-%s" % (pid, day, m.group(1), m.group(2)))
        if last and a < last + travel:
            lich.append("%s không kịp giờ" % pid)
        if money != p["ticket_adult_vnd"] * people:
            budget.append("%s giá khác dữ liệu" % pid)
        tien["an_uong" if meal else "ve"] += money
        if meal:
            meals.append(pid)
        else:
            sights += 1
        pos, last, pending = pid, b, None
    close_day()
    if index != n_days:
        lich.append("số ngày trong lịch khác ràng buộc")
    c = re.search(r"CHI PHÍ: ăn uống ([\d.]+) đ · vé ([\d.]+) đ · đi lại trong thành phố ([\d.]+) đ · Nội Bài khứ hồi "
                  r"([\d.]+) đ · dự phòng 10% ([\d.]+) đ", output)
    t = re.search(r"TỔNG ([\d.]+) đ", output)
    if not c or not t:
        budget.append("thiếu bảng chi phí")
    else:
        eat, ticket, move, air, reserve = [num(x) for x in c.groups()]
        total = num(t.group(1))
        want_air = 2 * airport(rb["khu_o"], people) if rb["di_may_bay"] == "1" else 0
        if (eat, ticket, move) != (tien["an_uong"], tien["ve"], tien["di"]):
            budget.append("khoản chi không bằng tổng các dòng")
        if air != want_air:
            budget.append("tiền Nội Bài sai")
        if reserve != int(round((eat + ticket + move + air) * 0.1)) or total != eat + ticket + move + air + reserve:
            budget.append("dự phòng hoặc tổng sai")
        if total > cap:
            budget.append("vượt trần của câu thử")
    return lich, budget


def main(argv):
    if len(argv) != 1:
        print(__doc__)
        return 2
    with open(argv[0], encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    n = ok_l = ok_b = 0
    for r in rows:
        res = check(r["id"], r.get("output", ""))
        if res is None:
            if RB.get(r["id"], {}).get("co_lich") == "co":
                print("%s không có lịch dù câu thử chờ lịch (chấm ở hanh_vi_dung)" % r["id"])
            continue
        n += 1
        lich, budget = res
        ok_l += not lich
        ok_b += not budget
        print("%s · lich_hop_le %s · ngan_sach_dung %s" % (
            r["id"], "đạt" if not lich else "; ".join(lich), "đạt" if not budget else "; ".join(budget)))
    print("Output có lịch: %d · lich_hop_le %d/%d · ngan_sach_dung %d/%d" % (n, ok_l, n, ok_b, n))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
