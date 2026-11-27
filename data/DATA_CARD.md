# Data card — dữ liệu bản chạy thử dùng

> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Ôn lại: ngày 6 · lab ngày 6. Chấm ở rubric R4.
> Một trang. Mỗi dataset một mục. Dữ liệu chạy thử để trong thư mục `data/` này.
> Không commit nguyên tài liệu khoá, dữ liệu cá nhân thật hay nguyên file data BTC cấp — chỉ đoạn trích ngắn, bản viết lại, hoặc số đã tổng hợp.

## Dataset 1 · Bộ dữ liệu Du lịch Hà Nội chuẩn theo format Kaggle (`vietnam_travel_hanoi.csv`)

| | |
|---|---|
| **Dùng để làm gì** | File CSV chuẩn hóa theo **đúng 12 cột format** của dataset Kaggle `vietnam_travel_central1.csv` (`region, province, url, video_id, title, channel, published_at, view_count, tags, transcript_status, transcript, ai_summary`), phục vụ tra cứu văn bản/RAG và làm chuẩn đối chiếu cho kho tri thức Hà Nội. |
| **Từ đâu** | - Khung schema 12 cột: lấy chuẩn từ `vietnam_travel_central1.csv`, không đưa vào repo (thuộc bộ Kaggle [`vietnam-travel-youtube-transcripts-and-ai-summaries`](https://www.kaggle.com/datasets/huythoi/vietnam-travel-youtube-transcripts-and-ai-summaries/data); lưu ý file `vietnam_travel_central1.csv` chỉ chứa 153 video Miền Trung nên không có dữ liệu Hà Nội).<br>- Nội dung 58 mục Hà Nội: tổng hợp và đối chiếu từ nguồn công khai chính thức năm 2025–2026 (Bộ Quốc phòng, Hoàng thành Thăng Long, Bảo tàng Lịch sử Quốc gia, Bảo tàng Mỹ thuật, Bảo tàng Hồ Chí Minh, Bảo tàng Thiên nhiên, Bảo tàng Hà Nội, Vườn thú Hà Nội, Vinpearl, Lotte World, Cà phê Giảng, Transerco, Grab, Vietnam Tourism, MIA, Klook, VNGuide, Foody...). |
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
| **Số dòng / số đoạn** | `hanoi_travel_kb.json`: **58 mục** · `hanoi_places.csv`: **50 dòng** (30 tham quan + 20 quán ăn; gồm 8 điểm có ngày đóng cửa định kỳ/cuối tuần và 9 điểm có giờ nghỉ trưa/bán theo ca) · `noi_bai_transfers.csv`: **8 dòng**. |
| **Phiên bản / ngày lấy** | `v2.0.0` · đối chiếu ngày `2026-11-27` |
| **Nhãn** | Đồng bộ với Dataset 1 (`thật` + `synthetic` ước tính). |
| **Giới hạn** | Tập trung ở nội thành Hà Nội và 2 điểm ngoại thành tiêu biểu (Bát Tràng - Gia Lâm, Đường Lâm - Sơn Tây); tọa độ và thời lượng gợi ý chỉ dùng ước tính lập lịch mẫu. |

## Dataset 3 · Mẫu bài VOZ (`evidence/voz-labels.csv`)

| | |
|---|---|
| Dùng để làm gì | đào bằng chứng pain · nguồn trích 7 câu thử `nguoi_dung` |
| Từ đâu | trang 1 của 5 thread công khai trên voz.vn |
| Xử lý những bước gì | lấy số bài, ngày, gắn 4 nhãn, giữ trích ngắn cho 7 bài; không lưu tên và toàn văn |
| Số dòng | 98 |
| Phiên bản / ngày lấy | 27/11/2026 |
| Nhãn | thật · nhãn do Claude Code gắn, chờ người kiểm |
| Giới hạn | xem `evidence/data-mining.md` mục 5 |

## Đối chiếu lại ngày 27/11/2026 (trường `verification` trong JSON)

Địa điểm và quán (50): trang chính thức đủ giá và giờ 7 · trang chính thức chỉ giờ 3 · báo chí 1 · thứ cấp 1 · nguồn phụ chưa mở trang 6 · mâu thuẫn 1 · **chưa kiểm 31**. Phương án Nội Bài (8): theo trang sân bay 5 · chưa kiểm 3.

| Mã | Nguồn | Mức | Ghi chú |
|---|---|---|---|
| HN-ATTR-01 Lăng Chủ tịch Hồ Chí Minh | [nguồn](https://tuoitre.vn/tam-dung-to-chuc-vao-lang-vieng-chu-tich-ho-chi-minh-tu-ngay-4-9-de-tu-bo-dinh-ky-100260809174846229.htm) | báo chí | Giờ mùa lạnh 01/11-31/03; mở lại 03/11/2026; nghỉ thứ Hai, thứ Sáu. Trang bqllang.gov.vn không truy cập được |
| HN-ATTR-02 Văn Miếu - Quốc Tử Giám | [nguồn](https://vanmieu.gov.vn/) | trang chính thức, giá và giờ | Vé người lớn 70.000đ, 08:00-17:00 mọi ngày. Tour đêm (thứ Tư, thứ Bảy, Chủ nhật) vé riêng, không tính trong dữ liệu |
| HN-ATTR-03 Hoàng thành Thăng Long | [nguồn](https://hoangthanhthanglong.vn/gia-ve-tham-quan-hoang-thanh-thang-long/) | trang chính thức, giá và giờ | Vé 100.000đ từ 01/01/2025; giờ 08:00-17:00 mọi ngày lấy ở trang chủ cùng website |
| HN-ATTR-04 Di tích Nhà tù Hỏa Lò | [nguồn](https://hoalo.vn/Home/Ve) | trang chính thức, giá và giờ | Vé 50.000đ; giờ 08:00-17:00 mọi ngày lấy ở trang chủ |
| HN-ATTR-05 Bảo tàng Dân tộc học Việt Nam | [nguồn](https://vme.vass.gov.vn/) | trang chính thức, giá và giờ | 40.000đ, 08:30-17:30, nghỉ thứ Hai và Tết |
| HN-ATTR-07 Bảo tàng Phụ nữ Việt Nam | [nguồn](https://baotangphunu.org.vn/tham-quan/) | trang chính thức, chỉ giờ | Giờ 08:00-17:00 mọi ngày khớp; trang không ghi giá vé |
| HN-ATTR-09 Bảo tàng Lịch sử Quốc gia | [nguồn](https://baotanglichsu.vn/vi/Articles/3108/ve-va-le-phi) | trang chính thức, giá và giờ | 40.000đ; đóng mọi thứ Hai (dữ liệu cũ ghi mở) |
| HN-ATTR-12 Bảo tàng Hồ Chí Minh | [nguồn](https://baotanghochiminh.vn/thong-tin-ve-tham-quan.htm) | trang chính thức, giá và giờ | Miễn phí cho khách Việt Nam, 40.000đ khách quốc tế (trang đăng 03/07/2018); giờ và ngày nghỉ lấy ở trang chủ |
| HN-ATTR-14 Bảo tàng Thiên nhiên Việt Nam | [nguồn](https://vnmn.ac.vn/) | nguồn mâu thuẫn, tạm loại | Trang chủ ghi đóng thứ Hai, thứ Ba, Chủ nhật; trang tham quan đoàn ghi thứ Ba đến thứ Sáu. Tạm không xếp lịch |
| HN-ATTR-15 Bảo tàng Hà Nội | [nguồn](https://baotanghanoi.com.vn/dang-ky-tham-quan/) | trang chính thức, chỉ giờ | 09:00-17:00, nghỉ thứ Hai (dữ liệu cũ ghi 08:00); trang không ghi giá |
| HN-ATTR-17 Thủy cung Vinpearl Aquarium Times City | [nguồn](https://vinwonders.com/vi/vinke-vinpearl-aquarium/) | trang chính thức, chỉ giờ | Giờ khớp; giá vé chưa kiểm |
| HN-ATTR-19 Vườn thú Hà Nội | [nguồn](https://vuonthuhanoi.com/) | trang chính thức, giá và giờ | 50.000đ; cổng mùa đông 07:30-22:00, khu trưng bày 08:00-16:00; lịch dùng giờ khu trưng bày |
| HN-ATTR-21 Không gian đi bộ Hồ Hoàn Kiếm & phụ cận | [nguồn](https://www.vietnamairlines.com/vn/vi/plan-book/travel/travel-guide/pho-di-bo-ha-noi) | nguồn thứ cấp (tóm tắt tìm kiếm) | 19:00 thứ Sáu đến 24:00 Chủ nhật; chưa có nguồn chính quyền |
| HN-FOOD-01 Phở Thìn 13 Lò Đúc | [nguồn](https://kamereo.vn/blog/vi/pho-thin-ha-noi/) | nguồn phụ, chưa mở trang | Các nguồn phụ khác nhau; giờ lấy khoảng hẹp để tránh đến lúc đóng cửa. Chưa mở trang xác nhận |
| HN-FOOD-02 Phở Gia Truyền 49 Bát Đàn | [nguồn](https://kamereo.vn) | nguồn phụ, chưa mở trang | Các nguồn phụ khác nhau; giờ lấy khoảng hẹp để tránh đến lúc đóng cửa. Chưa mở trang xác nhận |
| HN-FOOD-04 Phở Gà Nguyệt | [nguồn](https://guide.michelin.com/my/en/ha-noi/ha-noi_2974158/restaurant/pho-ga-nguyet) | nguồn phụ, chưa mở trang | Các nguồn phụ khác nhau; giờ lấy khoảng hẹp để tránh đến lúc đóng cửa. Chưa mở trang xác nhận |
| HN-FOOD-05 Bún Chả Hương Liên | [nguồn](https://mia.vn/cam-nang-du-lich/bun-cha-pho-co-ha-noi-20906) | nguồn phụ, chưa mở trang | Các nguồn phụ khác nhau; giờ lấy khoảng hẹp để tránh đến lúc đóng cửa. Chưa mở trang xác nhận |
| HN-FOOD-12 Xôi Yến | [nguồn](https://www.foody.vn/ha-noi/xoi-yen-nguyen-huu-huan) | nguồn phụ, chưa mở trang | Các nguồn phụ khác nhau; giờ lấy khoảng hẹp để tránh đến lúc đóng cửa. Chưa mở trang xác nhận |
| HN-FOOD-18 Bánh Mì 25 | [nguồn](https://www.foody.vn/ha-noi/banh-mi-25-hang-ca) | nguồn phụ, chưa mở trang | Các nguồn phụ khác nhau; giờ lấy khoảng hẹp để tránh đến lúc đóng cửa. Chưa mở trang xác nhận |
| HN-NBA-01 Xe buýt nhanh chất lượng cao số 86 | [nguồn](https://noibaiairport.vn/vi/transportation?tab=international) | trang sân bay, không ghi ngày | Giá và giờ theo bảng của sân bay (trang không ghi ngày, đang cập nhật); các trang thương mại ghi khác |
| HN-NBA-02 Xe buýt nhanh chất lượng cao số 68 | [nguồn](https://noibaiairport.vn/vi/transportation?tab=international) | trang sân bay, không ghi ngày | Giá và giờ theo bảng của sân bay (trang không ghi ngày, đang cập nhật); các trang thương mại ghi khác |
| HN-NBA-03 Xe buýt công cộng trợ giá tuyến 07 | [nguồn](https://noibaiairport.vn/vi/transportation?tab=international) | trang sân bay, không ghi ngày | Giá và giờ theo bảng của sân bay (trang không ghi ngày, đang cập nhật); các trang thương mại ghi khác |
| HN-NBA-04 Xe buýt công cộng trợ giá tuyến 17 | [nguồn](https://noibaiairport.vn/vi/transportation?tab=international) | trang sân bay, không ghi ngày | Giá và giờ theo bảng của sân bay (trang không ghi ngày, đang cập nhật); các trang thương mại ghi khác |
| HN-NBA-05 Xe buýt công cộng trợ giá tuyến 90 | [nguồn](https://noibaiairport.vn/vi/transportation?tab=international) | trang sân bay, không ghi ngày | Giá và giờ theo bảng của sân bay (trang không ghi ngày, đang cập nhật); các trang thương mại ghi khác |

Đơn giá đi lại (`city_transport`): [Grab, cập nhật 08/07/2026](https://www.grab.com/vn/en/blog/bang-thong-tin-cac-dich-vu-tren-ung-dung-grab/), GrabBike 13.255 đ / 2 km đầu, 4.222 đ/km, 344 đ/phút; GrabCar 4 chỗ 28.473, 9.818, 442.

## Chưa kiểm được

| Mục | Vì sao |
|---|---|
| 31 địa điểm và quán: ATTR-06, ATTR-08, ATTR-10, ATTR-11, ATTR-13, ATTR-16, ATTR-18, ATTR-20, ATTR-22, ATTR-23, ATTR-24, ATTR-25, ATTR-26, ATTR-27, ATTR-28, ATTR-29, ATTR-30, FOOD-03, FOOD-06, FOOD-07, FOOD-08, FOOD-09, FOOD-10, FOOD-11, FOOD-13, FOOD-14, FOOD-15, FOOD-16, FOOD-17, FOOD-19, FOOD-20 | không tìm thấy trang nguồn trong thời gian có; `source_url` vẫn là trang chủ |
| Giá vé của HN-ATTR-07, 15, 17 | trang chính thức không ghi |
| HN-NBA-06 đến 08 (taxi, xe công nghệ từ sân bay) | chỉ thấy giá "từ" trên trang đặt xe thương mại, khác khoảng trong dữ liệu |
| Bus Nội Bài | trang sân bay khác nhiều trang thương mại (bus 86: 35.000 / 45.000 / 50.000 đ); chỉ có giờ phía sân bay |
| Bảo tàng Lịch sử Quân sự | trang chính thức đang tắt |
| Phí nền tảng, giá giờ cao điểm của Grab | không đọc được nguyên văn |
| Thời lượng tham quan | ước tính (`synthetic`) |
| Dataset 1 | link `../vietnam_travel_central1.csv` không có trong repo |

## Dataset 4 · Quãng đường (`data/road_distances.json`)

| | |
|---|---|
| Dùng để làm gì | tiền và thời gian từng chặng trong `codebase/tools.py`, `eval/cham_code.py` |
| Từ đâu | tọa độ: OpenStreetMap Nominatim · quãng đường: OSRM demo server, hồ sơ driving · © OpenStreetMap contributors (ODbL) |
| Xử lý | 50 địa điểm (46 khớp đúng điểm, 4 chỉ khớp tên đường) và 10 điểm đại diện khu; ma trận 60 × 60 km |
| Phiên bản / ngày lấy | 27/11/2026 |
| Giới hạn | đường ô tô, xe máy có thể đi ngắn hơn; không tính tắc đường; vài điểm cách đường gần nhất tới khoảng 250 m; so với công thức chim bay × 1,3 trước đó, trung vị lệch 1,07 lần |
