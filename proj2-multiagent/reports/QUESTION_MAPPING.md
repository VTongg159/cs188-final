# Đối chiếu Project 2 trước triển khai — 16/11/2026

Ưu tiên [đề Spring 2026](https://inst.eecs.berkeley.edu/~cs188/sp26/projects/proj2/).
Đọc README và multiAgents.py của [repository Irrelev4nt13](https://github.com/Irrelev4nt13/The-Pac-Man-Projects-CS188-Berkeley), không chạy hoặc sửa repository đó.

| Question | Yêu cầu Spring 2026 | GitHub tham khảo | Hướng triển khai riêng |
|---|---|---|---|
| Q1, 4đ | Đánh giá state-action, openClassic 10 ván | Đã có: score + nghịch đảo Manhattan đến food, ±∞ terminal, ghost gần; giả định food không rỗng | Score, số food, khoảng cách food qua tường, tránh ghost hoạt động, đuổi scared khi còn thời gian, phạt STOP; terminal hữu hạn |
| Q2, 5đ | MAX Pacman, nhiều MIN ghost, depth tăng sau trọn vòng, đếm successor đúng | Đã có helper trả [value, action], chuẩn hóa agentIndex ở đầu đệ quy | Helper nội bộ trả value/action; next-agent modulo N; chỉ tăng depth khi về agent 0; first legal tie |
| Q3, 5đ | Alpha-beta, đúng thứ tự và không prune khi bằng | Đã có kiểm tra v > beta / v < alpha, không reorder | Cận truyền xuyên các ghost MIN, sinh con ngay trước đánh giá, cutoff nghiêm ngặt |
| Q4, 5đ | Chance node lấy trung bình đều legal moves | Đã có expectimax đệ quy, chia số action; chưa xử lý tập legal rỗng | Trung bình đều, cùng quy ước depth, xử lý terminal và không legal, evalFn cấu hình |
| Q5, 6đ | State evaluation, food/ghost/scared/capsule, smallClassic 10 ván | Đã có nhưng README tham chiếu Spring 2022; phạt STOP đếm legal STOP và trừ số âm nên thực tế cộng điểm; chưa xét food rỗng | Đặc trưng khoảng cách/số lượng, hệ số giải thích được, không suy luận hành động đã chọn từ legalActions; dùng terminal hữu hạn để tránh trung bình ∞ và -∞ |

README tham khảo có liên kết sp22; không coi đây là cùng phiên bản Spring
2026. Các class tương đồng không chứng minh scaffold/bộ chấm giống nhau.
Không sao chép lời giải; starter phải tải trực tiếp Berkeley.

## Cấu trúc và bảo toàn

Theo lựa chọn mới nhất của người dùng, toàn bộ Project 2 nằm trong
`Project2-Multiagent/`, gồm `multiagent/`, `results/`, `reports/`, `scripts/`,
`sources/`, `exports/`. Không tạo thư mục kết quả/báo cáo dùng chung ở gốc.
Project 1 chỉ được đọc để tính hash. Workspace/Project 1 chưa phải Git
repository; lỗi Git và trạng thái sẵn có của repo tham khảo được lưu trong
`sources/git-before.json`. Hash toàn bộ file là căn cứ kiểm tra độc lập.

## Khai báo AI

Dự án tự học có Codex đọc đề/mã tham khảo, viết mã mới trên starter,
kiểm thử, đo lường và soạn tài liệu. Không tuyên bố đây là bài sinh viên tự
viết không có AI. Chính sách Spring 2026 yêu cầu tự viết bài nộp, AI chỉ tư
vấn và không xem lời giải của người khác; quy trình tự học này không đáp ứng
điều kiện tác giả của bài nộp chính thức. Cần khai báo trung thực Q6 trên
Gradescope; Codex không tự điền hoặc nộp. Giữ nguyên giấy phép Berkeley.

## Cập nhật 22/11/2026: đơn giản hóa code và dùng môi trường chung

Bảng trên mô tả phiên bản trước. Code đã được viết lại cho đơn giản hơn, với sự hỗ trợ của Claude Code:

- Q1: score + 10/khoảng cách Manhattan tới food gần nhất, đuổi ghost đang sợ, phạt nặng khi ghost hoạt động ở sát bên, phạt STOP.
- Q2–Q4: mỗi agent tách thành `getAction`, `maxValue` và `minValue`/`expValue`. Depth tăng sau khi ghost cuối cùng đi.
  Alpha-beta chỉ cắt khi `>`/`<` nghiêm ngặt.
- Q5: score, khoảng cách tới food gần nhất, số food/capsule còn lại, đuổi ghost đang sợ, tránh ghost hoạt động.

Autograder vẫn đạt 25/25 (Q1 trung bình ~1240, Q5 trung bình ~1273, cả hai thắng 10/10).
