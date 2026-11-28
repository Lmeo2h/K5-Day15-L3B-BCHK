# Cách đếm khảo sát

Script: `python evidence/survey/count.py <file CSV>`. Câu hỏi: `questions.md`. Kết quả: `summary.md`.

## Mốc thời gian (đọc trước khi tin các mốc bên dưới)

- Form nhận câu trả lời từ **18:13 ngày 27/11**.
- Bản đầu của file này viết lúc 22:52 và commit lúc 23:16, theo bộ câu hỏi nháp. Người viết (Claude Code) chưa xem câu trả lời, nhưng lúc đó form đã có phần lớn câu trả lời và thành viên nhóm có thể đã xem. Câu "viết trước khi mở câu trả lời" ở bản đầu vì vậy không chứng minh được.
- Bản này sửa khoảng 23:45, **sau khi đọc dữ liệu**, vì form thật khác bộ nháp.

| Giữ từ bản đầu | Đổi sau khi thấy dữ liệu |
|---|---|
| Ngưỡng ≥20 người đúng người dùng; dưới 20 chỉ ghi x/N | Việc được đếm lấy theo câu 5 của form thật: đóng cửa hoặc hết giờ · đi vòng · đổi lịch vì thông tin sai hoặc chưa rõ. Bản nháp còn có "trả cao hơn" và "không biết đi gì từ sân bay", form thật không hỏi trong câu này |
| Loại người đang ở Hà Nội, người chưa đi | Chi vượt dự tính đếm riêng (câu 6). Cộng thêm vào số chính cũng không đổi kết quả |
| Mốc 20% người gặp ít nhất một việc, lấy từ mức đặt cho bài VOZ ở `../hypothesis.md` | Phút giữa khoảng theo lựa chọn thật: 15 · 45 · 120 · 240 |
| | Thêm hai nhóm con: đi từ TP.HCM · từ TP.HCM và mới đi một lần |

`../hypothesis.md` (viết 13:49) đặt hai điều kiện: phỏng vấn 2/3 người và ≥20% bài công khai. Khảo sát không nằm trong hai điều kiện đó, nên không dùng để thay chúng.

## Bản dữ liệu dùng để đếm

- Tải lúc **09:52 ngày 28/11/2026**: 36 câu trả lời, mẫu chính 24 người.
- So với bản tải lúc 23:59 ngày 27/11, nhóm đã **xoá 18 dòng** khỏi sheet vì không xác minh được người trả lời: 14 dòng gửi dồn trong khoảng 23:49 đến 23:57 và 4 dòng gửi trước đó.
- Còn 5 dòng gửi dồn từ 00:21 đến 00:25 ngày 28/11 (dòng 20 đến 24 trong `results.csv`). Nhóm xác nhận đó là người thật điền giúp; ngoài lời xác nhận này không có cách kiểm khác. Bỏ cả 5 dòng thì mẫu chính còn 19, dưới ngưỡng 20, và 16/19 gặp ít nhất một việc.

## Ai được tính (mẫu chính)

- Câu 1 chọn "có tham gia chuẩn bị" (đi một lần hoặc nhiều lần).
- Câu 2 chọn TP.HCM hoặc một tỉnh, thành khác ngoài Hà Nội.
- Người trong nhóm không điền.

## Đếm gì

| Số | Định nghĩa |
|---|---|
| Gặp ít nhất một việc (số chính) | Câu 5 chọn ≥1 trong ba việc ở bảng trên |
| Từng việc | x/N cho mỗi lựa chọn |
| Chi vượt dự tính | Câu 6 chọn một trong hai mức "cao hơn dự tính" |
| Thời gian tìm thông tin | Phân bố câu 4; trung bình theo phút giữa khoảng *(tự ước tính)*, dùng cho `spec.md` §2 |

## So với bài VOZ

Bài VOZ (N = 98): thiếu thông tin 12 · trả cao hơn dự kiến 3 · trái tuyến 0 · đóng cửa 0. Hai nguồn hỏi khác nhau nên không so phần trăm trực tiếp. Chỗ lệch ghi ở `../summary.md` mục 4.

## Dữ liệu cá nhân

Form không hỏi họ tên, email, số điện thoại. `results.csv` bỏ dấu thời gian; câu tự viết chỉ giữ khi người trả lời đồng ý cho trích; tên sự kiện nhận ra người viết được thay bằng `[một cuộc thi]`. File tải gốc để ngoài repo.
