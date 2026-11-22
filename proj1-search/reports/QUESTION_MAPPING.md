# Đối chiếu trước khi triển khai — 16/11/2026

Nguồn ưu tiên: https://inst.eecs.berkeley.edu/~cs188/sp26/projects/proj1/
Starter: https://inst.eecs.berkeley.edu/~cs188/sp26/assets/projects/search.zip
Tham khảo: https://github.com/Irrelev4nt13/The-Pac-Man-Projects-CS188-Berkeley
Commit tham khảo: e735a659767b9585575e03c56deb53b07c78665f.

| Câu | Repository tham khảo | Spring 2026 / quyết định triển khai riêng |
|---|---|---|
| Q1 | DFS, Stack, explored, truy vết cha; chưa chặn node đã pop trước khi mở rộng | Cùng API; dùng bản ghi đường đi trên Stack, bỏ bản sao đã mở rộng khi pop |
| Q2 | BFS, Queue, dict cha; biểu thức `child not in (explored and nodeParentAction)` khó đọc, phụ thuộc phép `and` trả toán hạng | Cùng bài toán; đánh dấu discovered ngay khi enqueue |
| Q3 | UCS với PriorityQueue.update, đóng explored vĩnh viễn | Cùng API và chi phí thay đổi; dùng best-g, bỏ entry lỗi thời |
| Q4 | A*; nhánh cải thiện so sánh `new_g + h(child) < old_g` | API tương đồng; so sánh g với g, cho phép mở lại trạng thái khi g giảm |
| Q5 | `(position, tuple(corners_remaining))`; start chưa loại góc đang đứng | Dùng `(position, visited_mask)` bất biến, xử lý góc tại start; tối đa 16V trạng thái |
| Q6 | Cộng Manhattan theo thứ tự góc gần nhất; README khẳng định hợp lệ nhưng lập luận chưa đủ | Tìm minimum trên mọi thứ tự góc trong bài toán Manhattan bỏ tường; có chứng minh relaxation; ngưỡng 2000/1600/1200 |
| Q7 | Max khoảng cách mê cung đến từng thức ăn, gọi mazeDistance và cache theo cặp | Dùng khoảng cách mê cung và MST thức ăn + khoảng cách đến thức ăn gần nhất, cache bản đồ BFS/tập thức ăn; ngưỡng 15000/12000/9000/7000 |
| Q8 | BFS trên AnyFoodSearchProblem, goal bằng food[x][y] | Cùng ý tưởng chuẩn phù hợp bài toán; tự viết trong starter chính thức |
| Q9 | Không thấy trong README Project 1 của repo | Spring 2026 thêm khai báo AI/cộng tác trên Gradescope, không phải bài lập trình/autograder cục bộ |

## Giới hạn xác minh

Không có bằng chứng repository cộng đồng thuộc học kỳ Spring 2026. Chưa chạy
autograder trên repo đó để tránh tạo file hay thay đổi trạng thái của repo.
Tương đồng API không có nghĩa test và toàn bộ scaffold giống nhau; sẽ đối chiếu
byte với ZIP và ghi nhận trong sources/starter-comparison.json. Không lấy repo
cộng đồng làm nền tảng hoặc sao chép lời giải.

## Khai báo sử dụng AI và chính sách

Đây là dự án tự học riêng do người dùng yêu cầu. Codex đọc đề, phân tích mã
tham khảo, viết lời giải mới, chạy kiểm thử, làm benchmark và soạn báo cáo.
Không thể mô tả sản phẩm này là bài làm không có AI của một sinh viên.
Chính sách Spring 2026 xem GenAI là công cụ tư vấn, yêu cầu tự viết bài nộp
và cấm đọc lời giải người khác; quy trình tự học có xem repo và AI viết mã
ở đây không đáp ứng điều kiện tác giả của bài nộp chính thức. Q9 trên
Gradescope chưa và sẽ không được tự động nộp. Không công khai lời giải;
giữ nguyên thông tin bản quyền Berkeley trong starter.

Nguồn chính sách: https://inst.eecs.berkeley.edu/~cs188/sp26/policies/#genai-policy

## Cập nhật 22/11/2026: đơn giản hóa code và dùng môi trường chung

Bảng trên mô tả phiên bản trước. Code đã được viết lại cho đơn giản hơn, với sự hỗ trợ của Claude Code:

- Q1–Q4: mỗi thuật toán là một hàm riêng. Frontier lưu `(state, actions)` (UCS/A* thêm `cost`), bỏ qua state đã expand khi pop.
- Q5: state là `(position, tuple các góc chưa đi qua)`.
- Q6: duyệt mọi thứ tự các góc còn lại (tối đa 4! = 24) theo khoảng cách Manhattan.
- Q7: khoảng cách mê cung tới food xa nhất (`mazeDistance`, cache theo cặp vị trí). trickySearch mở 4137 nút, vẫn dưới ngưỡng 7000.
- Q8: BFS trên `AnyFoodSearchProblem`.

Q5 và Q7 bây giờ trùng ý tưởng với repository tham khảo ở bảng trên. Đây là các cách giải phổ biến của bài.
Autograder vẫn đạt 26/25.
