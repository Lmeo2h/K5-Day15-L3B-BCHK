# Data card — dữ liệu bản chạy thử dùng

> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Ôn lại: ngày 6 · lab ngày 6. Chấm ở rubric R4.
> Một trang. Mỗi dataset một mục. Dữ liệu chạy thử để trong thư mục `data/` này.
> Không commit nguyên tài liệu khoá, dữ liệu cá nhân thật hay nguyên file data BTC cấp — chỉ đoạn trích ngắn, bản viết lại, hoặc số đã tổng hợp.

## Dataset 1 · Bộ dữ liệu Du lịch Hà Nội chuẩn theo format Kaggle (`vietnam_travel_hanoi.csv`)

| | |
|---|---|
| **Dùng để làm gì** | File CSV chuẩn hóa theo **đúng 12 cột format** của dataset Kaggle `vietnam_travel_central1.csv` (`region, province, url, video_id, title, channel, published_at, view_count, tags, transcript_status, transcript, ai_summary`), phục vụ tra cứu văn bản/RAG và làm chuẩn đối chiếu cho kho tri thức Hà Nội. |
| **Từ đâu** | - Khung schema 12 cột: lấy chuẩn từ [vietnam_travel_central1.csv](../vietnam_travel_central1.csv) (thuộc bộ Kaggle [`vietnam-travel-youtube-transcripts-and-ai-summaries`](https://www.kaggle.com/datasets/huythoi/vietnam-travel-youtube-transcripts-and-ai-summaries/data); lưu ý file `vietnam_travel_central1.csv` chỉ chứa 153 video Miền Trung nên không có dữ liệu Hà Nội).<br>- Nội dung 58 mục Hà Nội: tổng hợp và đối chiếu từ nguồn công khai chính thức năm 2025–2026 (Bộ Quốc phòng, Hoàng thành Thăng Long, Bảo tàng Lịch sử Quốc gia, Bảo tàng Mỹ thuật, Bảo tàng Hồ Chí Minh, Bảo tàng Thiên nhiên, Bảo tàng Hà Nội, Vườn thú Hà Nội, Vinpearl, Lotte World, Cà phê Giảng, Transerco, Grab, Vietnam Tourism, MIA, Klook, VNGuide, Foody...). |
| **Xử lý những bước gì** | 1. Đối chiếu thông tin giờ mở/đóng cửa, ngày nghỉ, nghỉ trưa, giá vé/giá món, tuyến buýt/taxi Nội Bài từ nguồn công khai.<br>2. Chuẩn hóa vào `hanoi_travel_kb.json`, kiểm tra toàn vẹn schema bằng `python data/build_and_validate.py`.<br>3. Kết xuất sang `vietnam_travel_hanoi.csv` đúng 12 cột (`region = "Miền Bắc"`, `province = "Hà Nội"`, `transcript_status = "ok (web verified kb)"`, `view_count` để trống không bịa số, `transcript` chứa đầy đủ thông số tra cứu, `ai_summary` tóm tắt 2–3 câu). |
| **Số dòng / số đoạn** | **58 dòng dữ liệu** (+1 dòng tiêu đề): **30** điểm tham quan + **20** quán ăn đặc trưng + **8** phương án di chuyển Nội Bài–trung tâm Hà Nội. |
| **Phiên bản / ngày lấy** | `v2.0.0` · đối chiếu ngày `2026-11-27` |
| **Nhãn** | Hỗn hợp (`thật` cho địa chỉ, giờ mở/đóng cửa, ngày nghỉ, giá vé/cước xe trích nguồn công khai; `synthetic` cho `suggested_duration_min`, `approx_lat`/`approx_lng` và dải giá 7 chỗ quy đổi). |
| **Giới hạn** | - `video_id` lưu mã bản ghi (`HN-ATTR-*`, `HN-FOOD-*`, `HN-NBA-*`) và `view_count` để trống vì đây là bản ghi đối chiếu web chính thức thay vì transcript video YouTube; `vietnam_travel_central1.csv` gốc chỉ phủ Miền Trung.<br>- Không phải dữ liệu thời gian thực (giá Grab/Xanh SM biến động theo giờ cao điểm/mưa, giờ mở cửa lễ Tết có thể thay đổi).<br>- **Bộ dữ liệu này dùng để chạy thử và đánh giá công cụ, không phải bằng chứng pain của người dùng.** |

## Dataset 2 · Kho tri thức có cấu trúc JSON & bảng phẳng (`hanoi_travel_kb.json`, `hanoi_places.csv`, `noi_bai_transfers.csv`)

| | |
|---|---|
| **Dùng để làm gì** | Nguồn dữ liệu có cấu trúc cho các công cụ tính toán bằng code trong `codebase/tools.py` (`tra_dia_diem`, `kiem_tra_mo_cua`, `tra_di_chuyen_noi_bai`, `uoc_tinh_di_chuyen`, `kiem_lich_trinh`) nhằm tránh LLM tự nhẩm giờ mở cửa và tiền vé. |
| **Từ đâu** | Cùng nguồn kiểm chứng với Dataset 1; các trường `suggested_duration_min`, `approx_lat`/`approx_lng` và dải giá 7 chỗ quy đổi là ước tính tổng hợp (`synthetic_estimate`) được kiểm tra 100% qua script `data/build_and_validate.py`. |
| **Xử lý những bước gì** | Chuẩn hóa lịch mở cửa 7 thứ (`opening_hours_by_day`), danh sách `closed_days`, `lunch_break`, `cost_min_vnd`/`cost_max_vnd`, `indoor_outdoor`, `rain_safe`, `kid_friendly` và xuất 2 bảng CSV phẳng (`utf-8-sig`). |
| **Số dòng / số đoạn** | `hanoi_travel_kb.json`: **58 mục** · `hanoi_places.csv`: **50 dòng** (30 tham quan + 20 quán ăn; gồm 7 điểm có ngày đóng cửa định kỳ/cuối tuần và 9 điểm có giờ nghỉ trưa/bán theo ca) · `noi_bai_transfers.csv`: **8 dòng**. |
| **Phiên bản / ngày lấy** | `v2.0.0` · đối chiếu ngày `2026-11-27` |
| **Nhãn** | Đồng bộ với Dataset 1 (`thật` + `synthetic` ước tính). |
| **Giới hạn** | Tập trung ở nội thành Hà Nội và 2 điểm ngoại thành tiêu biểu (Bát Tràng - Gia Lâm, Đường Lâm - Sơn Tây); tọa độ và thời lượng gợi ý chỉ dùng ước tính lập lịch mẫu. |
