# Reflection — Lê Quân Bảo

1. Vai trò + phần mình làm (trỏ tới file / commit):

- Thành viên, phụ trách sản phẩm và bằng chứng pain: `canvas.md`, `evidence/`.
- Canvas và giả thuyết CP1 (`a820351`), bằng chứng VOZ và canvas CP2 (`9c71af5`).
- Làm Google Form khảo sát, xoá khỏi bảng trả lời những dòng không xác minh được, đưa kết quả vào repo (`f45eed9`, `7d7060e`).
- Đưa phiếu kiểm tay nhãn VOZ 34 bài vào repo (`6e42f90`, `e2e835f`), đẩy giao diện web và phần cải tiến (`4ef5ea9`, `bdbf007`, `bbbe826`).

2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):

- Claude Code viết bản nháp tài liệu, code giao diện, script đếm, slide và video demo; mình giao việc, xem kết quả và yêu cầu sửa.
- Slide bản đầu nền be làm ảnh chụp không đọc được, mình yêu cầu làm lại nền trắng, khung ảnh tối.
- Cách đếm khảo sát bản đầu viết theo bộ câu hỏi nháp, phải viết lại theo form thật.
- Câu "AI gợi ý" trên lịch sai khoảng cách và buổi, mình yêu cầu sửa; giờ câu đó do code dựng từ dữ liệu.

3. Một câu thử trượt của nhóm và mình học được gì từ nó:

- B01: "Mình ở TP.HCM, lần đầu ra Hà Nội 2 ngày..." bị trả "Phần ngoài Hà Nội mình không hỗ trợ" vì model coi nơi xuất phát là nơi muốn đi.
- Đó đúng là người dùng nhóm nhắm tới. Câu thử phải viết theo cách người dùng thật kể, gồm cả chỗ họ đang ở.
- Model đọc sai được, nên cần code đối chiếu kết quả đọc với tin nhắn.
- Sửa xong lỗi đó, lượt 2 câu này vẫn trượt vì tự cộng tiền Nội Bài, đến lượt 3 mới đạt. Sửa một lỗi xong phải chấm lại cả câu.
