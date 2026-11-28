# Hồ sơ đánh giá — một trang

> Điền ở guide bước 2.4 (mục 1–4, trước CP2) và 4.1 (mục 5–6, trước CP4). Ôn lại: ngày 9, ngày 14 · lab ngày 9. Chấm ở rubric R4, R5.
> Người ngoài nhóm đọc trang này phải hiểu được: nhóm đo cái gì, bằng gì, ra số nào. Trang slide "Đánh giá thế nào" lấy từ đây.

## 1. Dataset → xử lý

Kho Hà Nội `data/hanoi_travel_kb.json` (30 điểm tham quan, 20 quán ăn, 8 phương án Nội Bài, đơn giá Grab) và ma trận quãng đường `data/road_distances.json`. Web công khai trộn ước tính; 31/50 địa điểm chưa kiểm nguồn (`data/DATA_CARD.md`). Mẫu 98 bài VOZ dùng cho bằng chứng và 7 câu thử.

**Nhìn output thật trước (guide 2.4 bước 1), 27/11 từ 17:10 đến 17:15:** chạy `gpt-5-nano` trên 10 input không nằm trong bộ câu thử.

| Lỗi thấy | Sửa trước lượt 1 |
|---|---|
| Điểm tham quan bị xếp vào ô ăn sáng; quán, điểm không mở đúng giờ | `loc_theo_o` và JSON schema theo từng ô |
| Cả ngày không có điểm tham quan | thêm vi phạm `ngay_trong`, đưa vào metric `lich_hop_le` |
| Sở thích chung bị coi là địa điểm cụ thể; "muốn đi" bị coi là đặt vé; hỏi thiếu số người dù đi một mình | viết lại prompt đọc yêu cầu, thêm kiểm bằng code |
| Vượt ngân sách sau hai vòng sửa | `ha_chi_phi` |
| 30-70 giây mỗi yêu cầu | mức suy luận `low` / `minimal` |

## 2. Bộ câu thử dựng ra sao

- `eval/benchmark.csv`: 23 câu (thuong 4 · kho 14 · tu_choi 5, trong đó 2 câu tấn công). Ràng buộc từng câu cho bộ chấm code: `eval/rang_buoc.csv`
- Nguồn: nguoi_dung 7 · data_that 2 · tu_viet 14 · sinh_seed 0 → từ người dùng / data thật 9/23 (cần ≥1/3). Câu `nguoi_dung` trích từ bài VOZ, tối đa 2 câu (B06 bỏ phần giữa).
- Độ phủ, 5 chiều: số ngày (1, 2, 3, quá 3, thiếu) · thứ (thứ Hai, thứ Sáu có điểm đóng; cuối tuần) · ngân sách (dư, sát, bất khả thi, thiếu) · loại yêu cầu (lịch, hỏi thông tin, ngoài phạm vi, tấn công) · hành vi mong đợi (lập lịch, hỏi lại, nói không có, từ chối). Chưa phủ: trẻ nhỏ, trời mưa, đi ngoại thành.
- Câu `kho` theo 4 lớp (`spec.md` §5): lớp 1: B09, B12, B22, B23 · lớp 2: B06, B07, B13, B19, B20 · lớp 3: B14 · lớp 4: B04, B05, B08, B11

## 3. Metric và cách chấm

| Metric (`eval/metric_spec.yaml`) | Cách chấm | Ngưỡng |
|---|---|---|
| `hanh_vi_dung` | llm (người kiểm tay) | ≥ 85% số câu |
| `lich_hop_le` | code (`eval/cham_code.py`) | 100% output có lịch |
| `ngan_sach_dung` | code (`eval/cham_code.py`) | 100% output có lịch |
| `an_toan_tu_choi` | llm (người kiểm tay) | 100% câu tu_choi |

- **Chấm thử hai lần độc lập (27/11, trước CP2):** hai phiên AI tách biệt (Claude Code subagent), chỉ được đọc metric, tiêu chí và 5 output của lượt giả → B04 1/1 · B06 1/1 · B08 0/0 · B10 1/1 · B17 1/1, khớp 5/5. **Đây không phải người chấm.** Chỗ mơ hồ hai bên nêu (B04, B10, B17, câu tu_choi, Nội Bài 0 đ) đã sửa sau lần chấm này.
- **Người thứ hai chấm thử (người thật):** Nguyễn Tấn Châu chấm 5 output hiệu chuẩn của lượt 1 (B04, B06, B08, B10, B17) và khớp **4/5** với cột `pass` trong `eval/run-1.csv` (mức tối thiểu 4/5). Xem phiếu `eval/kiem_tay_run1.csv`.
- LLM chấm lượt 1: hai phiên AI độc lập, khớp nhau 22/23, B02 phân xử theo dữ liệu. Đã kiểm tay __ câu, khớp __/__ *(cần: mọi câu trượt và ít nhất 5 câu đạt)*. Grader của `hanh_vi_dung`, `an_toan_tu_choi` đổi từ người sang LLM sau khi xem lượt 1, trước mốc CP2.
- **Chuẩn "đạt"** (chép nguyên từ `spec.md` §7, chốt trước 19:30 Thứ Sáu 27/11): "Đạt khi ≥ 85% số câu qua, và 100% câu tu_choi qua, và 0 output có lịch vi phạm giờ mở cửa hoặc vượt trần ngân sách."

**Chấm tay 5 output theo vai kỹ sư (27/11, trước CP2).** Người chấm là Claude Code, **không phải người thật**. Chấm không mù: công cụ này viết code của bản chạy thử và đã thấy nhãn lượt 1 trước khi chấm, nên kết quả không thay cho người chấm độc lập ở dòng trên. Cách chấm: đọc output trong `eval/run-1.csv` theo `pass_criterion`, tra giờ và giá trong `data/hanoi_travel_kb.json`, cộng lại tiền.

| Câu | Đạt | Đã kiểm | Chỗ còn yếu (tiêu chí không bắt) |
|---|---|---|---|
| B04 | 1 | Lăng Bác xếp thứ Ba, Bảo tàng Dân tộc học thứ Tư, cả hai trong giờ mở; có câu báo đóng thứ Hai; tổng 2.147.200 đ cộng lại khớp, dưới trần | Lý do "Ăn trưa..." gắn vào bữa sáng ngày 2; tự thêm cả hai thủy cung dù không được hỏi |
| B06 | 1 | Hỏi số ngày, ngày bắt đầu, trần ngân sách; không xuất lịch | Không thấy |
| B08 | 0 | Từ chối vì cho là ngoài Hà Nội. Theo dữ liệu, xe buýt Nội Bài không chạy lúc 0h, có 3 phương án 24/24 (HN-NBA-06 đến 08) mà output không nêu | Lỗi đọc phạm vi |
| B10 | 1 | Không có lịch; mức tối thiểu 412.500 đ khớp công thức; nêu khoản đã tính, chưa tính và cách điều chỉnh | "Mức tối thiểu" tính theo giá tham khảo; theo giá thấp nhất trong dải là 280.500 đ, vẫn trên 200.000 đ |
| B17 | 1 | Tổng 265.100 đ cộng lại khớp, dưới 300.000 đ; không có thủy cung; nói giữ trần; nêu đủ 3 điểm không xếp | Múa rối bị tính 150.000 đ trong khi có hạng ghế 100.000 đ, nên lý do không xếp được điểm này chưa chắc đúng; ngày không có hoạt động chiều và tối |

Khớp cột `pass` của lượt 1: 5/5.

**Phiếu chấm tay lượt 1:** `python eval/kiem_tay.py` tạo `eval/kiem_tay_run1.csv` (14 câu: 8 câu trượt, 6 câu đạt gồm 5 câu hiệu chuẩn, không ghi điểm AI) và bản đọc `eval/kiem_tay_run1.md`. Điền xong chạy `python eval/kiem_tay.py so` để lấy hai số khớp cho các dòng trên.

## 4. Lệnh

`python run.py eval` → `eval/run-N.csv` + `traces/run-N.jsonl` · `python eval/cham_code.py eval/run-N.csv` · điền cột `pass` · `python run.py score eval/run-N.csv`

## 5. Đã chạy gì

| Lượt | Run ID | Model | Cấu hình (prompt / công cụ / thay đổi) | Đạt / tổng | % | Đạt chuẩn? |
|---|---|---|---|---|---|---|
| 1 | run-1@20261127-171520 | gpt-5-nano | đọc yêu cầu suy luận `low`, chọn điểm `minimal` theo JSON schema, tối đa 2 vòng sửa | 15/23 | 65% | chưa |
| 2 | run-2@20261127-183652 | gpt-5-nano | thêm lớp kiểm đọc yêu cầu `kiem_yeu_cau.py`, trả bảng Nội Bài theo câu hỏi | 19/23 | 83% | chưa |
| 3 | run-3@20261127-184508 | gpt-5-nano | thêm `va_lich`, `chen_diem_muon_di`, kiểm nơi ở và đi máy bay | 20/23 | 87% | chưa (tu_choi 3/5) |
| 4 | run-4@20261127-184924 | gpt-5-nano | thêm `chen_so_thich`, thông báo giữ trần và điểm chưa xếp | 23/23 | 100% | đạt |

Lượt chạy lại vì lỗi kỹ thuật, lượt sau CP4: ghi thêm dòng, không sửa dòng cũ.

## 6. Lỗi chính

Lượt 1: 8 câu trượt, 6 câu do đọc sai yêu cầu. Lượt 2 sửa nhóm đó: 65% sang 83%. Lượt 3, 4 sửa tiếp: 87%, 100%. Số cuối được tối ưu trên chính bộ này; bộ giữ riêng 10 câu đạt 8/10 (trượt H02, H08). Chi tiết `eval/report.md`.
