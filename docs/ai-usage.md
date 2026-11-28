# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Claude Code | Viết `agent.py`, `tools.py`, `fake_model.py`, `eval/cham_code.py` | Chờ kiểm | Mai Xuân Khang |
| Prompt / thiết kế lời gọi mô hình | Claude Code | Soạn hai system prompt trong `agent.py`, sơ đồ `spec.md` §4 | Chờ kiểm | Mai Xuân Khang |
| Đào data (viết script đếm, gợi ý nhãn) | Claude Code | Tìm thread, viết cách đếm, gắn nhãn 98 bài, viết `count.py` | Kiểm tay __ dòng, khớp __ | Lê Quân Bảo |
| Đối chiếu dữ liệu | Claude Code | Đọc nguồn công khai, sửa giờ và giá, thêm đơn giá Grab, tọa độ OpenStreetMap, quãng đường OSRM | Chờ kiểm | Nguyễn Văn Hậu |
| Chấm thử 5 output (hiệu chỉnh tiêu chí) | Claude Code, hai subagent | Chấm độc lập, khớp 5/5, nêu chỗ mơ hồ | Kiểm tay 0 câu, chờ người chấm | Mai Xuân Khang |
| Chạy thử 10 input trên model thật, sửa prompt | Claude Code | Gom lỗi, sửa prompt, schema, công cụ | Chờ kiểm | Mai Xuân Khang |
| Cải tiến sau lượt 1, chạy lượt 2 đến 4, bộ giữ riêng | Claude Code | Viết code sửa, viết 10 câu giữ riêng, hai subagent chấm | Chờ kiểm | Mai Xuân Khang |
| Chấm tay 5 output theo vai kỹ sư (`eval/README.md` §3) | Claude Code | Đọc 5 output lượt 1, tra dữ liệu, cộng lại tiền; khớp 5/5, không mù | Chờ người thật chấm | Mai Xuân Khang |
| Mô phỏng chi phí 50 phiên | Claude Code | Chạy `run.py simulate`, điền `cost/cost-estimate.md` và `spec.md` §8 | Chờ kiểm | Nguyễn Văn Hậu |
| Giao diện web (`codebase/web.py`, `view.py`, `ui/`) | Claude Code | Thiết kế, viết code, tự thử bằng Edge không màn hình | Chờ kiểm | Mai Xuân Khang |
| Chuẩn bị CP3: đối chiếu trích dẫn, chia nhóm 12 bài, tìm số quy mô, script đếm khảo sát, phiếu chấm tay | Claude Code | Viết script, tải lại 5 thread, đọc 2 trang báo, viết lại pain và bảng impact | Chờ kiểm | Lê Quân Bảo |
| Video 30 giây CP3 | Claude Code | Viết kịch bản bấm tự động, quay màn hình giao diện gọi model thật theo thời gian thực, thêm phụ đề | Chờ xem lại | Nguyễn Tấn Châu |
| Thay câu lý do model viết bằng câu code dựng | Claude Code | Viết `_ly_do`, đổi nhãn giao diện, so output 23 câu trước và sau, chạy thử model thật, chụp lại ảnh slide | Chờ kiểm | Mai Xuân Khang |
| Video demo dự phòng CP4 | Claude Code · giọng đọc `gpt-4o-mini-tts` của OpenAI | Viết lời thuyết minh, tự bấm giao diện gọi model thật, quay hình, ghép giọng đọc và phụ đề; chỉ nhận lượt gọi model có đủ điểm tham quan mỗi ngày, lượt khác bị bỏ | Chờ xem lại | Nguyễn Tấn Châu |
| Slide CP4 (`slides/`, `demo-slides.pdf`) | Claude Code | Soạn 8 trang từ số trong repo, chụp hai kết quả thật, xuất PDF | Chờ kiểm | Nguyễn Tấn Châu |
| Phân tích khảo sát, viết lại pain và impact theo kết quả | Claude Code | Viết script đếm theo form thật, bỏ cột nhận dạng, cập nhật spec, canvas, slide | Chờ kiểm; nhóm xác nhận 5 dòng gửi dồn là người thật | Lê Quân Bảo |
| Soạn câu hỏi phỏng vấn | Claude Code | Soạn 6 câu | Chờ kiểm | Lê Quân Bảo |
| Viết câu thử (benchmark) | Claude Code | Viết 23 câu, gồm 7 câu trích từ bài VOZ | Chờ kiểm; cột `source` ghi nguồn | Mai Xuân Khang |
| Sinh data `synthetic` | Không dùng | | | |
| Chấm cột `pass` bằng LLM (nếu có) | Claude Code, hai subagent | Chấm độc lập 23 câu lượt 1, khớp 22/23 | Chưa người kiểm tay | Mai Xuân Khang |
| Slide, văn bản | Claude Code | Soạn `spec.md`, `canvas.md`, giả thuyết, tổng hợp bằng chứng | Chờ kiểm | Cả nhóm |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
