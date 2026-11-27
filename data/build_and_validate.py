"""Kiểm tra tính hợp lệ của hanoi_travel_kb.json và xuất ra các file CSV chuẩn.

Xuất ra:
  1. vietnam_travel_hanoi.csv — đúng 12 cột chuẩn của dataset Kaggle `vietnam_travel_central1.csv`
     (region, province, url, video_id, title, channel, published_at, view_count, tags, transcript_status, transcript, ai_summary)
  2. hanoi_places.csv — bảng phẳng 50 địa điểm & quán ăn cho kiểm đếm DATA_CARD.md
  3. noi_bai_transfers.csv — bảng phẳng 8 phương án di chuyển Nội Bài–trung tâm

Chạy từ thư mục gốc repo hoặc starter-repo:
    python data/build_and_validate.py [--validate-only]
"""
import csv
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
KB_PATH = DATA_DIR / "hanoi_travel_kb.json"
KAGGLE_HANOI_CSV = DATA_DIR / "vietnam_travel_hanoi.csv"
PLACES_CSV = DATA_DIR / "hanoi_places.csv"
TRANSFERS_CSV = DATA_DIR / "noi_bai_transfers.csv"

DAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")

KAGGLE_FORMAT_COLS = [
    "region",
    "province",
    "url",
    "video_id",
    "title",
    "channel",
    "published_at",
    "view_count",
    "tags",
    "transcript_status",
    "transcript",
    "ai_summary",
]

REQUIRED_PLACE_FIELDS = [
    "id",
    "name",
    "category",
    "sub_category",
    "district",
    "zone",
    "address",
    "approx_lat",
    "approx_lng",
    "opening_hours_summary",
    "opening_hours_by_day",
    "closed_days",
    "lunch_break",
    "best_time_of_day",
    "ticket_adult_vnd",
    "ticket_child_vnd",
    "cost_min_vnd",
    "cost_max_vnd",
    "price_note",
    "suggested_duration_min",
    "indoor_outdoor",
    "rain_safe",
    "kid_friendly",
    "kid_note",
    "tags",
    "highlights",
    "notes",
    "source_name",
    "source_url",
    "verified_date",
    "data_label",
]

REQUIRED_TRANSFER_FIELDS = [
    "id",
    "mode",
    "name",
    "route_summary",
    "target_zones",
    "operating_hours",
    "frequency_min",
    "duration_min_min",
    "duration_min_max",
    "fare_min_vnd",
    "fare_max_vnd",
    "fare_unit",
    "night_surcharge_note",
    "luggage_kid_friendly",
    "booking_method",
    "notes",
    "source_name",
    "source_url",
    "verified_date",
]


def validate_kb(kb: dict) -> dict:
    assert "places" in kb and "airport_transfers" in kb, "Thiếu khóa places hoặc airport_transfers"
    places = kb["places"]
    transfers = kb["airport_transfers"]

    seen_ids = set()
    attractions = 0
    foods = 0
    closed_edge_count = 0
    lunch_break_count = 0

    for item in places:
        for field in REQUIRED_PLACE_FIELDS:
            assert field in item, f"Place {item.get('id')} thiếu trường {field}"
        pid = item["id"]
        assert pid not in seen_ids, f"Trùng ID: {pid}"
        seen_ids.add(pid)

        assert item["category"] in ("attraction", "food"), f"Category lạ ở {pid}"
        if item["category"] == "attraction":
            attractions += 1
        else:
            foods += 1

        by_day = item["opening_hours_by_day"]
        assert set(by_day.keys()) == set(DAYS), f"{pid} thiếu ngày trong opening_hours_by_day"
        for day, val in by_day.items():
            assert val == "closed" or (isinstance(val, list) and len(val) > 0), f"{pid} sai định dạng giờ ngày {day}"

        assert item["cost_min_vnd"] <= item["cost_max_vnd"], f"{pid} cost_min > cost_max"
        assert item["indoor_outdoor"] in ("indoor", "outdoor", "mixed"), f"{pid} sai indoor_outdoor"

        if item["closed_days"]:
            closed_edge_count += 1
        if item["lunch_break"]:
            lunch_break_count += 1

    for item in transfers:
        for field in REQUIRED_TRANSFER_FIELDS:
            assert field in item, f"Transfer {item.get('id')} thiếu trường {field}"
        tid = item["id"]
        assert tid not in seen_ids, f"Trùng ID: {tid}"
        seen_ids.add(tid)
        assert item["fare_min_vnd"] <= item["fare_max_vnd"], f"{tid} fare_min > fare_max"
        assert item["duration_min_min"] <= item["duration_min_max"], f"{tid} duration_min > duration_max"

    return {
        "total_items": len(places) + len(transfers),
        "attractions": attractions,
        "foods": foods,
        "transfers": len(transfers),
        "places_with_closed_days": closed_edge_count,
        "places_with_lunch_break": lunch_break_count,
    }


def _place_to_kaggle_row(item: dict) -> dict:
    cat_label = "Tham quan" if item["category"] == "attraction" else "Ẩm thực"
    closed_txt = ", ".join(item["closed_days"]) if item["closed_days"] else "Không đóng ngày cố định"
    lunch_txt = item["lunch_break"] or "Không nghỉ trưa"
    rain_txt = "Có (phù hợp trời mưa)" if item["rain_safe"] else "Không (ngoài trời/dễ ảnh hưởng mưa)"
    kid_txt = f"Có ({item['kid_note']})" if item["kid_friendly"] else f"Hạn chế ({item['kid_note']})"
    highlights_txt = "; ".join(item["highlights"])

    transcript = (
        f"Mã: {item['id']} | Loại: {cat_label} ({item['sub_category']}) | Quận/Huyện: {item['district']} (zone: {item['zone']}). "
        f"Địa chỉ: {item['address']}. "
        f"Giờ mở cửa: {item['opening_hours_summary']}. Ngày đóng cửa: {closed_txt}. Nghỉ trưa: {lunch_txt}. "
        f"Chi phí/Giá vé: {item['price_note']} (ước tính người lớn: {item['ticket_adult_vnd']}đ, trẻ em: {item['ticket_child_vnd']}đ, dải chi phí: {item['cost_min_vnd']}-{item['cost_max_vnd']}đ). "
        f"Thời lượng gợi ý: {item['suggested_duration_min']} phút. Không gian: {item['indoor_outdoor']}. Tránh mưa: {rain_txt}. Trẻ nhỏ: {kid_txt}. "
        f"Điểm nổi bật: {highlights_txt}. Lưu ý: {item['notes']}"
    )
    ai_summary = (
        f"{item['name']} ({item['district']}, Hà Nội) thuộc nhóm {cat_label.lower()}, nổi bật với {highlights_txt}. "
        f"Lịch hoạt động: {item['opening_hours_summary']} (đóng cửa: {closed_txt}). "
        f"Chi phí tham khảo: {item['price_note']}"
    )
    tags = ",".join(["Hà Nội", "du lịch Hà Nội", item["district"], cat_label] + item["tags"])

    return {
        "region": "Miền Bắc",
        "province": "Hà Nội",
        "url": item["source_url"],
        "video_id": item["id"],
        "title": f"[{cat_label}] {item['name']} - {item['district']}, Hà Nội",
        "channel": item["source_name"],
        "published_at": item["verified_date"].replace("-", ""),
        "view_count": "",
        "tags": tags,
        "transcript_status": "ok (web verified kb)",
        "transcript": transcript,
        "ai_summary": ai_summary,
    }


def _transfer_to_kaggle_row(item: dict) -> dict:
    zones_txt = ", ".join(item["target_zones"])
    unit_txt = "người" if item["fare_unit"] == "per_person" else "chuyến/xe"
    fare_txt = (
        f"{item['fare_min_vnd']:,}đ/{unit_txt}"
        if item["fare_min_vnd"] == item["fare_max_vnd"]
        else f"{item['fare_min_vnd']:,}-{item['fare_max_vnd']:,}đ/{unit_txt}"
    )
    transcript = (
        f"Mã: {item['id']} | Loại: Di chuyển Nội Bài - Trung tâm ({item['mode']}). "
        f"Lộ trình: {item['route_summary']}. Khu vực phục vụ: {zones_txt}. "
        f"Giờ chạy: {item['operating_hours']} (tần suất ~{item['frequency_min']} phút/chuyến). "
        f"Thời gian di chuyển: {item['duration_min_min']}-{item['duration_min_max']} phút. "
        f"Giá cước: {fare_txt}. Hành lý & trẻ nhỏ: {'Phù hợp' if item['luggage_kid_friendly'] else 'Hạn chế khoang hành lý'}. "
        f"Đặt vé: {item['booking_method']}. Lưu ý đêm muộn: {item['night_surcharge_note']} Ghi chú: {item['notes']}"
    )
    ai_summary = (
        f"{item['name']} phục vụ tuyến Nội Bài về {zones_txt} trong khoảng {item['duration_min_min']}-{item['duration_min_max']} phút. "
        f"Giờ hoạt động: {item['operating_hours']}, mức giá {fare_txt}. {item['night_surcharge_note']}"
    )
    tags = ",".join(["Hà Nội", "Nội Bài", "di chuyển sân bay", item["mode"]] + item["target_zones"])

    return {
        "region": "Miền Bắc",
        "province": "Hà Nội",
        "url": item["source_url"],
        "video_id": item["id"],
        "title": f"[Nội Bài] {item['name']}",
        "channel": item["source_name"],
        "published_at": item["verified_date"].replace("-", ""),
        "view_count": "",
        "tags": tags,
        "transcript_status": "ok (web verified kb)",
        "transcript": transcript,
        "ai_summary": ai_summary,
    }


def build_kaggle_rows(kb: dict) -> list:
    rows = [_place_to_kaggle_row(p) for p in kb["places"]]
    rows.extend(_transfer_to_kaggle_row(t) for t in kb["airport_transfers"])
    return rows


def export_csvs(kb: dict) -> None:
    kaggle_rows = build_kaggle_rows(kb)
    with KAGGLE_HANOI_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=KAGGLE_FORMAT_COLS)
        writer.writeheader()
        writer.writerows(kaggle_rows)

    place_headers = [
        "id", "name", "category", "sub_category", "district", "zone", "address",
        "approx_lat", "approx_lng", "opening_hours_summary", "closed_days",
        "lunch_break", "best_time_of_day", "ticket_adult_vnd", "ticket_child_vnd",
        "cost_min_vnd", "cost_max_vnd", "price_note", "suggested_duration_min",
        "indoor_outdoor", "rain_safe", "kid_friendly", "tags", "notes",
        "source_name", "source_url", "verified_date", "data_label",
    ]
    with PLACES_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=place_headers)
        writer.writeheader()
        for item in kb["places"]:
            row = {k: item[k] for k in place_headers}
            row["closed_days"] = "|".join(item["closed_days"])
            row["tags"] = "|".join(item["tags"])
            row["lunch_break"] = item["lunch_break"] or ""
            writer.writerow(row)

    with TRANSFERS_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_TRANSFER_FIELDS)
        writer.writeheader()
        for item in kb["airport_transfers"]:
            row = dict(item)
            row["target_zones"] = "|".join(item["target_zones"])
            writer.writerow(row)


def main() -> None:
    import sys

    validate_only = "--validate-only" in sys.argv[1:]
    kb = json.loads(KB_PATH.read_text(encoding="utf-8"))
    stats = validate_kb(kb)
    if not validate_only:
        export_csvs(kb)
    print("Validation PASSED:", json.dumps(stats, ensure_ascii=False))
    if not validate_only:
        print(
            f"Exported: {KAGGLE_HANOI_CSV.name} ({stats['total_items']} rows), "
            f"{PLACES_CSV.name} ({len(kb['places'])} rows), "
            f"{TRANSFERS_CSV.name} ({len(kb['airport_transfers'])} rows)"
        )


if __name__ == "__main__":
    main()
