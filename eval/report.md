# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | run-1@20261127-171520 | 15/23 | 65% | 2/4 | 9/14 | 4/5 | chưa |
| 2 | run-2@20261127-183652 | 19/23 | 83% | 2/4 | 12/14 | 5/5 | chưa (dưới 85%) |
| 3 | run-3@20261127-184508 | 20/23 | 87% | 3/4 | 14/14 | 3/5 | chưa (tu_choi dưới 100%) |
| 4 | run-4@20261127-184924 | 23/23 | 100% | 4/4 | 14/14 | 5/5 | đạt |

- Cùng 23 câu, cùng metric, model `gpt-5-nano`. Câu thử, ràng buộc, metric và chuẩn "đạt" không đổi giữa các lượt.
- Metric code: lượt 1 `lich_hop_le` 6/7, `ngan_sach_dung` 7/7 · lượt 2 7/7, 5/7 · lượt 3 7/7, 7/7 · lượt 4 7/7, 7/7.
- Cột `pass`: hai phiên AI chấm độc lập (lượt 1 khớp 22/23, lượt 2 đến 4 khớp 23/23). **Chưa người kiểm tay.**
- **Số 100% của lượt 4 cao hơn thực lực:** ba vòng sửa đều dựa trên câu trượt của chính bộ này. Bộ giữ riêng 10 câu viết sau lượt 4, chạy một lần, đạt **8/10 (trượt H02, H08)** (`eval/giu_rieng.csv`, `eval/giu_rieng_ket_qua.csv`; người viết câu biết cách code hoạt động, một bộ chấm AI).
- Lần chạy lúc mất mạng 18:41 được khung ghi là `run-error`, không tính là một lượt.

Kết quả từng câu: `eval/run-N.csv`. Trace: `traces/run-N.jsonl`.

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
| B01 | "Mình ở TP.HCM, lần đầu ra Hà Nội 2 ngày..." | "Phần ngoài Hà Nội mình không hỗ trợ" | Model coi nơi xuất phát là yêu cầu đi ngoài Hà Nội |
| B15 | "Lên giúp lịch Đà Nẵng 3 ngày 4 triệu" | Một lịch Hà Nội 3 ngày | Model không đánh dấu ngoài phạm vi, code không có lớp kiểm thứ hai |
| B22 | "ra đó đi từ NB vào ks kiểu gì ạ?" | "Mình không có dữ liệu cho câu hỏi này" | Model đặt `di_may_bay=false` nên code không tra bảng Nội Bài |
| B03 | "bay ra Hà Nội... 3 ngày... 3 triệu" | Không đưa lịch, in mã lỗi `trung_diem` | Model chọn lại cùng một điểm và không sửa được |

## 3. Một lần cải tiến (lượt 1 sang lượt 2)

- Nhắm vào nhóm lỗi: đọc sai yêu cầu (phạm vi và câu hỏi sân bay, kèm điểm được gọi tên). Đau nhất vì người dùng bị từ chối yêu cầu hợp lệ, hoặc nhận lịch cho nơi họ không đi.
- Đã sửa: thêm `codebase/kiem_yeu_cau.py` đối chiếu kết quả đọc của model với tin nhắn; trả bảng Nội Bài theo câu hỏi (taxi, giờ, thuê xe).
- Kết quả: nhóm lỗi đó (B01, B08, B09, B11, B15, B22, B23) 0/7 sang 5/7 · tổng 65% sang 83%.
- Câu nào **tệ đi** sau khi sửa: B04.

**Các lượt chạy thêm:**
- Lượt 3: không tự thêm đi máy bay, chỉ nhận nơi ở khi nói rõ; `va_lich` vá điểm trùng, quán lặp, ngày trống; `chen_diem_muon_di`. Tổng 87%; B02, B17, B18 trượt.
- Lượt 4: `chen_so_thich`; nhận câu đòi phá quy tắc bằng luật; khi không xếp được thì nói giữ trần và nêu điểm chưa xếp. Tổng 100% trên bộ này.

## 4. Còn lại

- Câu lý do do model viết có lúc sai (gọi điểm cách 5,8 km là "gần", buổi sáng ghi "buổi chiều"). Nguy hiểm vừa: người đọc có thể tin lý do sai.
- Nội Bài: code chọn tuyến rẻ nhất **phục vụ khu ở** (19.000 đ) trong khi định nghĩa metric ghi "rẻ nhất"; cần nói rõ khi trình bày.
- Code chỉ dùng một giá tham khảo cho mỗi điểm. Điểm có nhiều hạng vé (múa rối 100.000 đến 200.000 đ) có thể bị báo không xếp được dù hạng rẻ vừa tiền.
- Lịch ngày đến không tính giờ hạ cánh; chợ Đồng Xuân có lúc xếp tối dù chợ trong nhà đóng 18:00.
- Luật đọc yêu cầu dùng danh sách địa danh và từ khoá, sẽ sót cách nói khác.
- Nếu có thêm 1 tuần: bộ giữ riêng do người ngoài nhóm viết, kiểm nguồn các điểm còn lại, tính giờ hạ cánh.
