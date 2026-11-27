# Tóm tắt mô phỏng simulate-1@20261127-184807

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| xep_mot_lan | 28 | 1 | 3689 | 785 | 1.3 | 2.0 |
| sua_nhieu_lan | 18 | 3 | 11594 | 2505 | 4.0 | 7.1 |
| xep_lai_khi_di | 4 | 5 | 26685 | 4988 | 8.0 | 25.5 |

Tỉ lệ đạt dùng để tính: 19/23 (83%) — lượt run-2@20261127-183652

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (500 người) | Chi phí / tháng — cơ sở (2.000 người) | Chi phí / tháng — cao (10.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-5-nano (vào 0.05 · ra 0.4 $/1M) | $0.0011 | $0.0013 | $0.00066 | $0.5532 | $2.21 | $11.06 | $0.0011 |
| gpt-5.4-mini (vào 0.75 · ra 4.5 $/1M) | $0.0141 | $0.0171 | $0.0084 | $7.01 | $28.03 | $140.15 | $0.0140 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (2.0) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gpt-5-nano. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
