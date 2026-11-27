# Cách đếm khảo sát (viết tối 27/11, trước khi mở câu trả lời)

Script: `python evidence/survey/count.py <file CSV xuất từ Google Forms>`. Câu hỏi: `questions.md`.

## Ai được tính (mẫu số N)

- Trả lời câu 1 là "TP.HCM" hoặc "tỉnh khác ngoài Hà Nội". Người sống ở Hà Nội hoặc chưa đến bao giờ không vào mẫu số.
- Người trong nhóm không điền. Câu trả lời trùng hệt mọi ô tính một lần.
- N dưới 20 thì chỉ ghi x/N, không ghi %, và khảo sát **chưa đạt ngưỡng**.
- Báo riêng số người đi từ TP.HCM và số chuyến trong 12 tháng qua.

## Đếm gì

| Số | Định nghĩa |
|---|---|
| Gặp ít nhất một sự cố (số chính) | Câu 6 chọn ≥1 trong: đến nơi thì đóng cửa · đi vòng, mất thời gian vì điểm xa nhau · trả cao hơn dự kiến · không biết đi gì từ sân bay, bến xe |
| Từng sự cố | x/N cho mỗi lựa chọn ở câu 6 |
| Thời gian lên lịch | Phân bố câu 4. Ước tính trung bình dùng cho `spec.md` §2: không lên lịch 0 phút · dưới 1 giờ 30 · 1-3 giờ 120 · trên 3 giờ 240 (giá trị giữa là *tự ước tính*) |
| Chi vượt dự tính | Câu 7 chọn "vượt dưới 20%" hoặc "vượt từ 20%" |

## Mốc đặt trước

- Giả thuyết được khảo sát ủng hộ nếu **≥20% người** trong mẫu gặp ít nhất một sự cố, cùng mức đã đặt cho bài VOZ ở `../hypothesis.md`.
- Câu 6 đưa sẵn lựa chọn nên người trả lời dễ chọn hơn so với tự kể trong diễn đàn. Hai con số không so trực tiếp; chỉ so **thứ tự** các sự cố.

## So với bài VOZ

Bài VOZ (N = 98): thiếu thông tin 12 · trả cao hơn dự kiến 3 · trái tuyến 0 · đóng cửa 0. Khớp nếu khảo sát cũng xếp "không biết đi gì" đứng đầu. Lệch thì ghi lại và giải thích, không đổi nhãn VOZ cho khớp.

## Dữ liệu cá nhân

Script bỏ cột dấu thời gian, email, tên, số điện thoại và che email, số điện thoại trong câu tự do, rồi mới ghi `results.csv`. File xuất gốc để ngoài repo. Đọc lại câu 8 trước khi commit.
