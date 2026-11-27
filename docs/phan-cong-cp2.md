# Phân công Checkpoint 2

Chỉ gồm việc của CP2. Hạn **19:30 Thứ Sáu 27/11**. Các file đã có bản nháp; việc của mỗi người là kiểm, làm nốt và giải thích được phần mình.

## File của từng người

| File | Chủ file |
|---|---|
| `spec.md` §3, §5, §6, §9, §10 | Châu |
| `README.md` | Châu |
| `eval/README.md` §3 (chấm thử) | Châu và Khang |
| `spec.md` §0, §1, §2 | Bảo |
| `canvas.md` | Bảo |
| `evidence/hypothesis.md`, `evidence/summary.md`, `evidence/data-mining.md` | Bảo |
| `evidence/voz-labels.csv`, `evidence/count.py`, `evidence/interviews/cau-hoi.md`, `evidence/survey/questions.md` | Bảo |
| `data/hanoi_travel_kb.json`, `data/road_distances.json`, `data/hanoi_places.csv`, `data/noi_bai_transfers.csv`, `data/vietnam_travel_hanoi.csv` | Hậu |
| `data/build_and_validate.py`, `data/DATA_CARD.md` | Hậu |
| `spec.md` §4, §7 | Khang |
| `codebase/agent.py`, `codebase/tools.py`, `codebase/ai.py`, `codebase/fake_model.py`, `.env` (trên máy, không commit) | Khang |
| `eval/benchmark.csv`, `eval/rang_buoc.csv`, `eval/metric_spec.yaml`, `eval/cham_code.py` | Khang |
| `eval/README.md` §1, §2, §4 | Khang |
| `docs/ai-usage.md` | Khang |

Mỗi người pull trước khi sửa. File trong `data/` vừa đổi nhiều (giờ, giá xe buýt, tọa độ, quãng đường), Hậu cần pull bản mới trước khi làm tiếp.

## Việc của từng người

### Nguyễn Tấn Châu: chỗ khó, rủi ro, nộp bài

| Việc | File | Xong trước |
|---|---|---|
| Phân mỗi người thử một sản phẩm tương tự 10 phút, thay chữ "chưa kiểm" | `spec.md` §3 | 18:30 |
| Đọc lại kịch bản khó, đường đi trải nghiệm, rủi ro; điền phòng, zone | `spec.md` §5, §6, §9, dòng tiêu đề | 18:30 |
| Chấm độc lập output B04, B06, B08, B10, B17, so với Khang, ghi số khớp (cần ít nhất 4/5) | `eval/README.md` §3 | 19:00 |
| Mở các link bằng cửa sổ ẩn danh rồi nộp CP2 | repo GitHub | 19:15 |

### Lê Quân Bảo: canvas, bằng chứng, người dùng

| Việc | File | Xong trước |
|---|---|---|
| Đọc lại 98 bài theo link, sửa nhãn sai, ghi số dòng khớp | `evidence/voz-labels.csv`, `evidence/data-mining.md` §5 | 18:30 |
| Chạy `python evidence/count.py`; số đổi thì cập nhật mọi nơi | `evidence/summary.md`, `canvas.md` dòng 4, `spec.md` §1, `eval/metric_spec.yaml` (báo Khang) | 18:40 |
| Mở link kiểm 7 trích dẫn | `evidence/data-mining.md` §4 | 18:40 |
| Gửi tin hẹn phỏng vấn, ghi vai và giờ | `evidence/summary.md` mục "Lịch hẹn" | 18:50 |
| Tạo Google Form từ bộ câu hỏi, gửi vào nhóm lớp | `evidence/survey/questions.md` | 18:00 |
| Dẫn nhóm chốt người dùng, rà bảng impact | `canvas.md`, `spec.md` §0-§2 | 19:00 |

### Nguyễn Văn Hậu: dữ liệu

| Việc | File | Xong trước |
|---|---|---|
| Đọc bảng "Đối chiếu lại", mở vài link kiểm | `data/DATA_CARD.md` | 18:00 |
| Kiểm điểm chưa có nguồn, ưu tiên điểm trong câu thử: Quân sự (06), Mỹ thuật (08), Ngọc Sơn (10), múa rối (16), Bát Tràng (20), chợ Đồng Xuân (26) | `data/hanoi_travel_kb.json` | 18:50 |
| Gọi hoặc xem fanpage các quán có giờ mâu thuẫn (01, 02, 04, 05, 12, 18) | `data/hanoi_travel_kb.json` | trước CP3 |
| Kiểm giá xe công nghệ, taxi từ Nội Bài (NBA-06 đến 08) bằng ứng dụng | `data/hanoi_travel_kb.json` | trước CP3 |
| Chạy `python data/build_and_validate.py`; sửa link Dataset 1 | `data/DATA_CARD.md`, ba file CSV | 19:00 |

### Mai Xuân Khang: thiết kế, khung chạy, đánh giá

| Việc | File | Xong trước |
|---|---|---|
| Tạo `.env` trên máy mình, chạy `python run.py` thử vài input, đọc bảng lỗi đã thấy | `.env`, `eval/README.md` | 18:20 |
| Kiểm tay mọi câu trượt và ít nhất 5 câu đạt của lượt 1, ghi số khớp | `eval/run-1.csv`, `eval/README.md` §3 | 19:00 |
| Đọc code, chạy thử, giải thích được luồng và công thức đi lại | `codebase/`, `spec.md` §4 | 18:30 |
| Duyệt 23 câu thử và ràng buộc | `eval/benchmark.csv`, `eval/rang_buoc.csv` | 18:45 |
| Chấm 5 output lần một | `eval/README.md` §3 | 18:50 |
| Chốt metric và chuẩn đạt cùng nhóm | `eval/metric_spec.yaml`, `spec.md` §7 | **19:10** |

## Cả nhóm chốt trước 19:10

1. Chuẩn đạt: "Đạt khi ≥ 85% số câu qua, và 100% câu tu_choi qua, và 0 output có lịch vi phạm giờ mở cửa hoặc vượt trần ngân sách."
2. Người dùng: giữ "từ TP.HCM, lần đầu" hay mở sang người từ tỉnh khác.
3. Giả định tiền: không gồm vé máy bay và chỗ ở, dự phòng 10%, Nội Bài hai chiều, đi lại tính theo công thức ở `spec.md` §4.

Sau 19:30 không sửa được chuẩn đạt và `eval/metric_spec.yaml`. Câu thử chỉ được thêm. Lát cắt chỉ được thu hẹp.

## Lỗi còn lại và cách sửa

| Lỗi | Cách sửa | Ai | Khi nào |
|---|---|---|---|
| Lượt 1 đạt 15/23 (65%), dưới chuẩn 85% | Đọc `eval/report.md`, chọn một cải tiến, chạy lượt 2 trên cùng bộ câu thử | Cả nhóm, Khang | trước CP4 |
| 6 câu trượt do đọc sai yêu cầu (B01, B08, B09, B15, B22, B23) | Ứng viên cải tiến: sửa prompt đọc yêu cầu, thêm lớp kiểm bằng code, hoặc dùng model mạnh hơn cho bước này | Khang | sau CP3 |
| Cột `pass` do hai AI chấm, chưa người kiểm | Kiểm tay, ghi số khớp; thấy sai thì sửa nhãn và ghi lại | Khang, Châu | trước CP3 |
| Chưa có người thứ hai là người thật chấm 5 output | Châu và Khang chấm độc lập | Châu, Khang | trước CP2 |
| Nhãn 98 bài chưa kiểm tay | Đọc lại, sửa, đếm lại | Bảo | trước CP2 |
| Bằng chứng 14,3% dưới ngưỡng 20%, một nguồn, bài cũ | Giữ số thật; phỏng vấn ít nhất 3 người, khảo sát ít nhất 20 người | Bảo, cả nhóm | trước CP3 |
| 31/50 địa điểm và 3/8 phương án Nội Bài chưa kiểm | Mở trang nguồn, gọi điện nơi mâu thuẫn | Hậu | trước CP4 |
| Quãng đường tính theo ô tô, không tính tắc đường | Ghi là giới hạn; đối chiếu vài chặng trên ứng dụng bản đồ | Hậu | trước CP4 |
| Chi phí mới thử 10 phiên, số người dùng tự ước tính | Tìm nguồn công khai, chạy `python run.py simulate` đủ 50 phiên | Hậu | trước CP4 |
| Thời gian trả lời 3-14 giây mỗi yêu cầu khi thử | Đo lại trên lượt 2 | Khang | trước CP4 |
| Spec: §3 chưa thử sản phẩm, impact tự ước tính, phòng và zone trống | Thử sản phẩm, thay số phỏng vấn | Châu, Bảo | §3 trước CP2, impact trước CP3 |
| Video 30 giây gọi model thật chưa quay | Quay màn hình `python run.py` | Châu | trước CP3 |
