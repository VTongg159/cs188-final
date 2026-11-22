# Project 3: nguồn và cách triển khai (22/11/2026)

Đề: https://inst.eecs.berkeley.edu/~cs188/sp26/projects/proj3/
Starter: https://inst.eecs.berkeley.edu/~cs188/sp26/assets/projects/reinforcement.zip (v1.001), commit `p3: add original starter code`.

| Câu | Điểm | Cách triển khai |
|---|---|---|
| Q1 Value Iteration | 5 | Batch value iteration: mỗi vòng tính `V_{k+1}` từ `V_k` cũ. `Q(s,a) = Σ T(s,a,s')[R(s,a,s') + γV(s')]`. Policy = argmax Q. |
| Q2 Bridge | 1 | discount 0.9, noise 0.0: không có nhiễu thì đi qua cầu an toàn. |
| Q3 Policies | 6 | 3a (0.3, 0, 0), 3b (0.3, 0.2, 0), 3c (0.9, 0, 0), 3d (0.9, 0.2, 0), 3e (0, 0, 1). Discount thấp: chọn exit gần. Có noise: tránh vực. Living reward dương: không thoát. |
| Q4 Prioritized Sweeping | 0 (thưởng) | Tìm predecessor, xếp state vào hàng đợi theo sai số `|V(s) − max Q(s,a)|`, cập nhật state sai nhiều nhất, đưa predecessor có sai số > θ vào lại hàng đợi. |
| Q5 Q-Learning | 5 | `Q(s,a) ← (1−α)Q(s,a) + α[r + γ max Q(s',a')]`, Q mặc định 0, chọn ngẫu nhiên khi hòa. |
| Q6 Epsilon-greedy | 2 | Với xác suất ε chọn hành động ngẫu nhiên, ngược lại chọn hành động tốt nhất. |
| Q7 Bridge revisited | 1 | `NOT POSSIBLE`: 50 episode không đủ để học policy tối ưu với xác suất > 99%. |
| Q8 Q-Learning Pacman | 1 | Dùng lại QLearningAgent, không cần code thêm. smallGrid thắng 100/100 sau 2000 ván train. |
| Q9 Approximate Q-Learning | 4 | `Q(s,a) = Σ w_i f_i(s,a)`, `w_i ← w_i + α·difference·f_i(s,a)`. |

Autograder local: 26/25 (Q4 là điểm thưởng).

## Môi trường chung

Framework của Project 3 giống framework của Project 2, nên Project 3 dùng chung `pacman_env/`.
Class `Experiences` (dữ liệu test) được chuyển nguyên văn từ `util.py` sang `experiences.py`.

## Khai báo sử dụng AI

Code Project 3 do Claude Code viết theo yêu cầu của nhóm, dựa trên đề và starter chính thức. Claude Code cũng chạy autograder và viết tài liệu này.
Đây là các cách giải chuẩn của bài. Trước khi nộp chính thức, cần khai báo trung thực việc dùng AI theo chính sách
Spring 2026: https://inst.eecs.berkeley.edu/~cs188/sp26/policies/#genai-policy
