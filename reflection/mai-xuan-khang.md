# Reflection — Mai Xuân Khang

1. Vai trò + phần mình làm (trỏ tới file / commit):

- Thành viên, phụ trách kiến trúc AI, `codebase/`, bộ câu thử, metric và báo cáo đánh giá.
- Code bản chạy thử, 23 câu thử, 4 metric và lượt 1 (`a31e7e5`).
- Ghi kết quả chấm tay lượt 1 (`553e1fc`) và link video demo dự phòng (`883e94a`).

2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):

- Dùng AI Agent viết bản đầu `agent.py`, `tools.py`, bộ chấm, câu thử, hai system prompt và các cải tiến sau lượt 1 (`docs/ai-usage.md`).
- Lượt 1 chỉ đạt 15/23: model đọc sai yêu cầu, phải thêm `kiem_yeu_cau.py` để code đối chiếu.
- Câu lý do model viết từng sai khoảng cách và buổi, đã thay bằng `_ly_do` dựng từ dữ liệu.
- Chấm tay phát hiện B02 và B04 xếp múa rối 19:00 không có suất, AI chấm đã bỏ sót.

3. Một câu thử trượt của nhóm và mình học được gì từ nó:

- B03: 3 ngày có Nội Bài, ngân sách 3 triệu. Model chọn trùng điểm tham quan; trace `run-2` cho thấy gửi lại vi phạm đến lượt thứ ba vẫn trùng nên không đưa lịch.
- Bài học: lỗi có luật rõ ràng như trùng điểm thì để code vá, đừng trông vào việc nhắc model.
- Lượt 3 thêm `va_lich`, câu này đạt. Model chọn điểm, code giữ ràng buộc.
