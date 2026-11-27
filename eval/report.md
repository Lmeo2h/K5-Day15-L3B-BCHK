# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | run-1@20261127-171520 | 15/23 | 65% | 2/4 | 9/14 | 4/5 | chưa |
| 2 | | __/__ | | __/__ | __/__ | __/__ | đạt / chưa |

- Model `gpt-5-nano`. Metric code (`python eval/cham_code.py eval/run-1.csv`): `lich_hop_le` 6/7 output có lịch (trượt B15) · `ngan_sach_dung` 7/7. B01 và B03 chờ lịch nhưng không ra lịch.
- Chuẩn đạt: 65% dưới 85%; câu `tu_choi` 4/5 dưới 100%.
- Cách chấm cột `pass`: hai phiên AI độc lập, khớp 22/23; B02 phân xử theo nhãn dữ liệu. **Chưa có người kiểm tay.**

Kết quả từng câu: `eval/run-1.csv`. Trace: `traces/run-1.jsonl`.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| Đọc sai phạm vi | 3 | B01, B08, B15 |
| Không nhận ra câu hỏi đi lại từ sân bay | 3 | B09, B22, B23 |
| Xếp trùng điểm, hai vòng sửa không khắc phục | 1 | B03 |
| Bỏ sót điểm được yêu cầu mà không báo | 1 | B11 |

**Lỗi cụ thể:**

| Câu | Input (rút gọn) | Output | Vì sao sai |
|---|---|---|---|
| B01 | "Mình ở TP.HCM, lần đầu ra Hà Nội 2 ngày..." | "Phần ngoài Hà Nội mình không hỗ trợ" | Model coi nơi xuất phát là yêu cầu đi ngoài Hà Nội (`ngoai_pham_vi=ngoai_ha_noi`) |
| B15 | "Lên giúp lịch Đà Nẵng 3 ngày 4 triệu" | Một lịch Hà Nội 3 ngày | Model để `ngoai_pham_vi=[]`, code không có lớp kiểm thứ hai |
| B22 | "ra đó đi từ NB vào ks kiểu gì ạ?" | "Mình không có dữ liệu cho câu hỏi này" | Model để `di_may_bay=false` nên code không tra bảng Nội Bài dù dữ liệu có |
| B03 | "bay ra Hà Nội... đến Nội Bài... 3 ngày... 3 triệu" | Không đưa lịch, in mã lỗi `trung_diem` | Model chọn lại cùng một điểm qua các ngày và không sửa được |

**Lỗi chất lượng không làm trượt câu:** câu lý do model viết sai ngữ cảnh (bữa sáng ghi "ăn trưa"); output lộ mã lỗi nội bộ; câu "hỏi lại" hoặc "không xếp được" chưa trỏ đúng nguyên nhân.

## 3. Một lần cải tiến

*Nhóm chọn sau khi đọc các câu trượt.* Ứng viên: nhóm "đọc sai yêu cầu" (đọc sai phạm vi và không nhận ra câu hỏi sân bay, 6/8 câu trượt).

- Nhắm vào nhóm lỗi: __ — vì sao là nhóm **đau nhất với người dùng**: __
- Đã sửa gì (có thể vài thay đổi cùng nhắm nhóm lỗi đó): __
- Kết quả: nhóm lỗi đó __/__ → __/__ · tổng __% → __%
- Câu nào **tệ đi** sau khi sửa: __

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào: __
- Nếu có thêm 1 tuần: __
