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
| Soạn câu hỏi phỏng vấn | Claude Code | Soạn 6 câu | Chờ kiểm | Lê Quân Bảo |
| Viết câu thử (benchmark) | Claude Code | Viết 23 câu, gồm 7 câu trích từ bài VOZ | Chờ kiểm; cột `source` ghi nguồn | Mai Xuân Khang |
| Sinh data `synthetic` (nếu có) | | | Seed __ · kiểm tay __ dòng | |
| Chấm cột `pass` bằng LLM (nếu có) | Claude Code, hai subagent | Chấm độc lập 23 câu lượt 1, khớp 22/23 | Kiểm tra thủ công __ câu thử, khớp __/__ | Mai Xuân Khang |
| Slide, văn bản | Claude Code | Soạn `spec.md`, `canvas.md`, giả thuyết, tổng hợp bằng chứng | Chờ kiểm | Cả nhóm |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
