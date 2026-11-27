# Đào data: bài viết công khai trên diễn đàn VOZ

> Guide bước 1.2. Script đếm: `evidence/count.py`. Bảng gắn nhãn: `evidence/voz-labels.csv`.

## 1. Cách đếm (viết lúc 16:15 ngày 27/11/2026, trước khi đọc mẫu)

- **Data dùng:** chủ đề (thread) công khai trên voz.vn, tìm bằng công cụ tìm kiếm web với các cụm "lần đầu ra Hà Nội", "du lịch Hà Nội tự túc voz", "đi Hà Nội tư vấn voz".
- **Chọn thread:** chủ đề nói về một người đến Hà Nội với tư cách khách (hỏi lịch trình, đi lại, chi phí, hoặc kể chuyện xảy ra trong chuyến đi). Lấy mọi thread tìm được thoả điều kiện, không chọn theo nội dung trả lời.
- **Trên tập nào:** mọi bài ở trang 1 của mỗi thread, gồm bài mở đầu và trả lời.
- **Mẫu số N:** số bài đã đọc và gắn nhãn, kể cả bài đùa hoặc không liên quan.
- **Đếm gì:** bài mà người viết tự nêu mình (hoặc người đi cùng) đã gặp hoặc đang vướng ít nhất một lỗi dưới đây. Lời khuyên cho người khác, câu đùa, bình luận không kể chuyện của mình thì không tính.

| Nhãn | Định nghĩa |
|---|---|
| `L1_thong_tin` | Phải hỏi hoặc không biết đi đâu, đi bằng gì, giá bao nhiêu |
| `L2_trai_tuyen` | Mất thời gian vì đi vòng, sai đường, xếp các điểm xa nhau |
| `L3_dong_cua` | Đến nơi thì đóng cửa hoặc ngoài giờ |
| `L4_chi_phi` | Trả cao hơn dự kiến, bị đòi thêm, bị tính giá cao |

- **Chạy lại:** `python evidence/count.py` đọc bảng nhãn và in x/N, %.
- **Đã biết trước khi viết cách đếm:** thành viên gắn nhãn đã xem tóm tắt thread "Lần đầu ra hà nội đã bị ăn chưởng" trong lúc tìm nguồn lúc khoảng 13:50.

## 2. Đọc trước, đếm sau

Lấy 5 thread (xem ngày 27/11/2026), 98 bài ở trang 1, của 69 tài khoản. Bài đăng từ 2022 đến 2024.

| Thread | Số bài | Link |
|---|---|---|
| 678405 "xin chỉ giáo, lần đầu đi HN" | 20 | https://voz.vn/t/xin-chi-giao-lan-dau-di-hn.678405/ |
| 820237 "Lần đầu ra Hà Nội cần tư vấn..." | 20 | https://voz.vn/t/lan-dau-ra-ha-noi-can-tu-van-cach-di-lai-tai-san-bay-va-khach-san.820237/ |
| 866081 "Lần đầu ra hà nội đã bị ăn chưởng" | 20 | https://voz.vn/t/lan-dau-ra-ha-noi-da-bi-an-chuong-huhu.866081/ |
| 948129 "Xin Tips đi Hà Nội 1 mình" | 18 | https://voz.vn/t/xin-tips-di-ha-noi-1-minh.948129/ |
| 1013476 "Du lịch Hà Nội một mình 1 tuần" | 20 | https://voz.vn/t/du-lich-ha-noi-mot-minh-1-tuan.1013476/ |

Làm rõ khi gắn nhãn: chỉ tính chuyện thuộc chuyến đến Hà Nội. Ba bài kể chuyện nơi khác hoặc không nói ở đâu bị loại (866081 bài #10, #12, #20; xem cột `ghi_chu`). Tính cả ba bài này thì tối đa 17/98.

## 3. Kết quả (`python evidence/count.py`)

| Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|
| Bài nêu ít nhất 1 lỗi | 14/98 | 14,3% | một bài có thể mang hai nhãn |
| L1 thiếu thông tin (đi đâu, đi bằng gì, giá) | 12/98 | 12,2% | |
| L4 trả cao hơn dự kiến | 3/98 | 3,1% | cả 3 thuộc cùng một sự việc ở thread 866081 |
| L2 trái tuyến | 0/98 | 0% | |
| L3 đóng cửa | 0/98 | 0% | |
| Tài khoản nêu ít nhất 1 lỗi | 8/69 | | chỉ đếm, không lưu tên |

## 4. Ví dụ nguyên văn (bỏ tên, tối đa 2 câu, xem ngày 27/11/2026)

1. "Thế là em tốn 350k thì mới được xuống xe, em ko dám làm căng vì mình từ xa đến, có quen biết ai đâu." (VOZ 866081 #1)
2. "Đi từ Sân bay Nội Bài về khu Láng Hạ ( Đại Sứ Quán Mỹ ) thì giá taxi khoảng bao nhiêu?" (VOZ 820237 #1)
3. "ra đó đi từ NB vào ks kiểu gì ạ?" (VOZ 678405 #1)
4. "gọi taxi hay grab có mắc quá k thím? lần đầu ra k biết thuê xe kiểu gì lun" (VOZ 678405 #6)
5. "Em không biết mình chia từng quận để đi có hợp lí không" (VOZ 1013476 #1)
6. "Tài chính 1m trụ đc mấy ngày với các yêu tố trên ạ" (VOZ 948129 #9)
7. "mai em có chuyến vietjet đến HN lúc 12h đêm. có bus nào về nội thành giờ đấy ko các bác nhỉ" (VOZ 820237 #19)

## 5. Giới hạn của data

- Thread được chọn vì là bài hỏi hoặc kể sự cố, nên tỷ lệ không đại diện cho mọi du khách.
- Chỉ đọc trang 1; thread 866081 còn nhiều trang.
- Bài cũ (2022-2024), không phải chuyện trong 1 tháng qua.
- Phần lớn không biết người viết đến từ đâu; thread 866081 tự nói từ Sài Gòn. Có người đi công tác, không phải du lịch.
- **Nhãn do Claude Code gắn, chưa được người kiểm tay.** TV2 đọc lại 98 bài theo `voz-labels.csv` rồi ghi số dòng khớp: __/98.

Kiểm lại bằng phỏng vấn theo `evidence/interviews/cau-hoi.md`.
