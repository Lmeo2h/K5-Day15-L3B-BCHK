# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): xếp một lần (60%, 1 lượt hỏi) · sửa nhiều lần (30%, 3 lượt) · xếp lại khi đi (10%, 5 lượt), mỗi người 1 phiên / tháng. Nguồn: *(tự ước tính)*, chờ khảo sát và phỏng vấn.
- **Số người dùng** 3 kịch bản: thấp 500 · cơ sở 2.000 · cao 10.000 người / tháng *(tự ước tính)*. Đối chiếu quy mô (`spec.md` §2): đường bay Hà Nội và TP.HCM 11,07 triệu ghế năm 2025 ([VnExpress, 24/12/2025, dẫn OAG](https://e.vnexpress.net/news/business/economy/hanoi-hcmc-remains-world-s-4th-busiest-flight-route-4997830.html)), từ đó ước khoảng 4.600 người đi chơi lần đầu, tự túc mỗi tháng *(tỉ lệ 1% là tự ước tính)*. Kịch bản cơ sở bằng khoảng 43% con số này; kịch bản cao giả định mở sang nơi xuất phát khác.
- **Giá** (USD / 1 triệu token, vào và ra): `gpt-5-nano` 0,05 và 0,40 · `gpt-5.4-mini` 0,75 và 4,50. [Trang giá OpenAI](https://developers.openai.com/api/docs/pricing), BTC xem 25/11/2026.
- **Tỉ lệ đạt** dùng để tính: 19/23 (83%), lượt `run-2`.
- Đo token trên model `gpt-5-nano`, tính giá `gpt-5-nano` và `gpt-5.4-mini`.

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-1.csv` · run ID `simulate-1@20261127-184807` · 50 phiên · seed 42 · 0 phiên lỗi · trung bình 11,8 giây / phiên.
Code đo là bản tại thời điểm lượt 3 (bắt đầu 18:48, trước thay đổi của lượt 4). Tỉ lệ đạt lấy ở lượt 2 theo rubric.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| xep_mot_lan | 28 | 1 | 3689 | 785 | 1.3 | 2.0 |
| sua_nhieu_lan | 18 | 3 | 11594 | 2505 | 4.0 | 7.1 |
| xep_lai_khi_di | 4 | 5 | 26685 | 4988 | 8.0 | 25.5 |

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (500 người) | Chi phí / tháng — cơ sở (2.000 người) | Chi phí / tháng — cao (10.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-5-nano (vào 0.05 · ra 0.4 $/1M) | $0.0011 | $0.0013 | $0.00066 | $0.5532 | $2.21 | $11.06 | $0.0011 |
| gpt-5.4-mini (vào 0.75 · ra 4.5 $/1M) | $0.0141 | $0.0171 | $0.0084 | $7.01 | $28.03 | $140.15 | $0.0140 |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt.

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): 120 phút tìm và ghép thông tin cho mỗi chuyến *(tự ước tính)*.
- Chi phí / người / tháng (cơ sở, `gpt-5-nano`): $0,0011.
- **Kết luận:** xét riêng tiền model thì đáng làm ($0,0011 so với 120 phút mỗi người), với điều kiện dữ liệu giữ được đúng và người dùng thật thấy lịch dùng được. Hai điều kiện này chưa đo.

## 4. *(Muốn sâu hơn, không bắt buộc)*

- Đổi sang `gpt-5.4-mini` giữ nguyên số token: chi phí tăng khoảng 13 lần (ước tính theo giá, chưa chạy thử).
- Chưa tính: máy chủ, công cập nhật giờ mở cửa và giá, công người kiểm.
