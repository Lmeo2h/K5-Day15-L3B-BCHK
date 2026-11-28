# Reflection — Nguyễn Văn Hậu

1. Vai trò + phần mình làm (trỏ tới file / commit):

- Thành viên, phụ trách dữ liệu Hà Nội và mô phỏng chi phí.
- Dữ liệu điểm tham quan, quán ăn, phương án Nội Bài và `data/DATA_CARD.md` trong `data/`.
- Kiểu người dùng và chi phí: `cost/personas.yaml`, `cost/cost-estimate.md`, lượt mô phỏng `simulate-1` 50 phiên.

2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):

- Claude Code đối chiếu nguồn công khai để sửa giờ và giá, thêm đơn giá Grab, toạ độ OpenStreetMap, quãng đường OSRM (`docs/ai-usage.md`).
- Claude Code chạy `run.py simulate` và điền bảng chi phí.
- Dữ liệu vẫn còn 31/50 địa điểm và 3/8 phương án Nội Bài chưa kiểm nguồn, nên không coi output là đã đúng.

3. Một câu thử trượt của nhóm và mình học được gì từ nó:

- B11, lượt 2: tám điểm trong một ngày. Tin nhắn không nói nơi ở nhưng model tự đoán Ba Đình, nên tiền xe chặng đi và chặng về sai, trượt metric `ngan_sach_dung`.
- Một giả định không ai thấy đã làm sai số tiền, dù đơn giá và quãng đường đều đúng.
- Bài học: thiếu thông tin thì dùng giá trị mặc định và nói rõ cho người dùng, không để model tự đoán.
- Lượt 3 chỉ nhận nơi ở khi tin nhắn nói rõ, câu này đạt.
