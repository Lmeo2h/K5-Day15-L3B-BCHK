# Tổng hợp bằng chứng pain

> Điền ở guide bước 1.2, xong trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1. Cập nhật sáng 28/11 theo bản khảo sát tải lúc 09:52.

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm ghi trước, chạy lại được, ≥5 ví dụ) | ☑ đạt · nhãn do AI gắn, **chưa kiểm tay** | `evidence/data-mining.md` |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☑ đạt: 36 câu trả lời, **24 người đúng điều kiện**; 5 trong số đó nhóm tự xác nhận (mục 4) | `evidence/survey/summary.md`, `results.csv`, `cach-dem.md` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☐ chưa phỏng vấn ai | `evidence/interviews/cau-hoi.md` |

## 2. Số chính

**Đào data:** **14/98 bài (14,3%)** trong 5 thread VOZ nêu ít nhất một lỗi. Thiếu thông tin 12/98 (đi lại và thuê xe 6, trong đó từ Nội Bài 4 · đi đâu, chia ngày, tiền 5 · giờ hàng quán 1) · trả cao hơn dự kiến 3/98 · trái tuyến 0/98 · đóng cửa 0/98. Chạy lại: `python evidence/count.py`, đối chiếu trích dẫn: `python evidence/verify_quotes.py`.

**Khảo sát,** mẫu chính 24 người đi từ ngoài Hà Nội và có chuẩn bị chuyến đi (17 người từ TP.HCM):

| Đếm gì | Mẫu chính | Từ TP.HCM |
|---|---|---|
| Gặp ít nhất một trong ba việc dưới | **18/24 (75%)** | 13/17 |
| Đến nơi mới biết đóng cửa hoặc hết giờ nhận khách | 9/24 | 8/17 |
| Đi vòng hoặc quay lại do cách xếp lịch | 9/24 | 6/17 |
| Đổi lịch vì thông tin sai hoặc chưa rõ | 4/24 | 2/17 |
| Chi cao hơn dự tính | 15/24 | 12/17 |
| Tìm thông tin từ 1 giờ trở lên | 12/24 | 8/17 |

Thời gian tìm thông tin trung bình theo phút giữa khoảng *(tự ước tính)*: 86 phút.

**Phỏng vấn:** 0/3, chưa có buổi nào.

## 3. Trích dẫn nguyên văn (có nguồn, bỏ tên)

1. "Thế là em tốn 350k thì mới được xuống xe, em ko dám làm căng vì mình từ xa đến, có quen biết ai đâu." (VOZ 866081 #1)
2. "Đi từ Sân bay Nội Bài về khu Láng Hạ ( Đại Sứ Quán Mỹ ) thì giá taxi khoảng bao nhiêu?" (VOZ 820237 #1)
3. "ra đó đi từ NB vào ks kiểu gì ạ?" (VOZ 678405 #1)
4. "gọi taxi hay grab có mắc quá k thím? lần đầu ra k biết thuê xe kiểu gì lun" (VOZ 678405 #6)
5. "Em không biết mình chia từng quận để đi có hợp lí không" (VOZ 1013476 #1)
6. "Tài chính 1m trụ đc mấy ngày với các yêu tố trên ạ" (VOZ 948129 #9)
7. "mai em có chuyến vietjet đến HN lúc 12h đêm. có bus nào về nội thành giờ đấy ko các bác nhỉ" (VOZ 820237 #19)

Từ khảo sát (người trả lời đồng ý cho trích; đủ các câu của mẫu chính ở `evidence/survey/summary.md`):

- "Mất gần 3 tiếng plan mà tới noi thì bị đóng cửa ;-;"
- "Lần đâu đi HN đi chơi xíu mà tới nơi thì quán đóng cửa, mất thời gian thật sự"
- "Mình lưu nhầm địa chỉ chi nhánh của quán, xuống xe mới phát hiện nên phải đặt thêm một chuyến sang đúng địa chỉ."

Link từng thread và ngày xem: `evidence/data-mining.md` mục 2.

## 4. Các nguồn có khớp nhau không

Chưa khớp.

| Điều được đếm | VOZ (N = 98) | Khảo sát (N = 24) |
|---|---|---|
| Đến nơi thì đóng cửa | 0/98 | 9/24 |
| Đi vòng, trái tuyến | 0/98 | 9/24 |
| Tiền | trả cao hơn dự kiến 3/98 | chi cao hơn dự tính 15/24 (hai câu hỏi khác nhau) |
| Thiếu thông tin | phải hỏi đi đâu, đi gì, giá 12/98 | đổi lịch vì thông tin sai hoặc chưa rõ 4/24 (hai câu hỏi khác nhau) |
| Đi từ Nội Bài | 4/98 hỏi | form không hỏi |

Cách giải thích *(chưa kiểm)*:
- Bài VOZ đã đọc phần lớn là câu hỏi trước chuyến đi, nên ít có chỗ để kể lỗi xảy ra trong chuyến.
- Khảo sát hỏi chuyến đã qua và đưa sẵn lựa chọn, nên người trả lời dễ chọn hơn so với tự kể. Người từng gặp trục trặc cũng có thể sẵn lòng điền hơn.

Giới hạn của khảo sát: N = 24, mẫu thuận tiện; không biết bao nhiêu người là "bạn trẻ" vì form không hỏi tuổi; nhóm đã xoá 18 dòng không xác minh được; 5 dòng gửi dồn từ 00:21 đến 00:25 ngày 28/11 chỉ được xác nhận bằng lời của nhóm, bỏ đi thì còn 16/19 và mẫu dưới 20 (`evidence/survey/cach-dem.md`).

## 5. Kết luận (sáng 28/11)

- **Khảo sát đạt ngưỡng:** 24 người đúng điều kiện, 18/24 gặp ít nhất một việc, trên mốc 20% ghi ở `evidence/survey/cach-dem.md` (mốc này ghi khi form đã có câu trả lời).
- Điều kiện đặt trước về bài công khai (≥20%) **không đạt**: 14,3%.
- Điều kiện về phỏng vấn (2/3 người) trong `evidence/hypothesis.md` chưa làm, nên giả thuyết gốc **chưa xác nhận đầy đủ**.
- Phần có ở cả hai nguồn: người đi phải tự tìm và ghép thông tin, và có lúc thông tin đó thiếu hoặc sai.
- Việc cần làm: phỏng vấn 3 người; khảo sát tiếp qua kênh kiểm được người trả lời.
