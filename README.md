# CS188 Sp26 — Bài tập lớn

Repo của nhóm cho bài tập lớn dựa trên môn **CS188: Introduction to Artificial Intelligence** (UC Berkeley, Spring 2026).
Nội dung gốc: <https://inst.eecs.berkeley.edu/~cs188/sp26/projects/>

Nhóm 3 người làm **Project 1, 2, 3 và 5** (bỏ Project 4).

| Thư mục | Project | Nội dung |
|---|---|---|
| `proj1-search/` | Project 1 — Search | DFS, BFS, UCS, A*, heuristic cho Pacman |
| `proj2-multiagent/` | Project 2 — Multi-Agent Search | Reflex agent, Minimax, Alpha-Beta, Expectimax |
| `proj3-rl/` | Project 3 — Reinforcement Learning | Value Iteration, Q-Learning, Approximate Q-Learning |
| `proj5-ml/` | Project 5 — Machine Learning | Perceptron, Neural Network, RNN, CNN (PyTorch) |
| `docs/` | — | Báo cáo, tài liệu chung của nhóm |

## Phân công

| Thành viên | GitHub | Phụ trách |
|---|---|---|
|  |  | Tạo repo, Project 5 |
|  |  |  |
|  |  |  |

## Quy ước làm việc

1. **Mỗi project một nhánh**: `proj1`, `proj2`, `proj3`, `proj5`. Không commit trực tiếp lên `main`.
2. **Merge vào `main` qua Pull Request**, có ít nhất một thành viên khác xem qua trước khi merge.
3. **Commit message** có tiền tố theo project:
   - `p1: ...`, `p2: ...`, `p3: ...`, `p5: ...` (ví dụ: `p5: implement PerceptronModel.run`)
   - Thay đổi chung (README, docs, .gitignore): `docs: ...` hoặc `chore: ...`
4. **Không sửa thư mục của người khác.** Nếu cần thay đổi, hãy báo người phụ trách hoặc mở issue.
5. Commit đầu tiên của mỗi project là **code gốc chưa sửa** (`pX: add original starter code`) để dễ xem diff.
6. Không commit file model (`*.pt`, `*.pth`), `__pycache__/`, cấu hình editor — đã có trong `.gitignore`.

### Quy trình cơ bản

```bash
git checkout main && git pull
git checkout proj5            # hoặc: git checkout -b proj5 (lần đầu)
# ... sửa code ...
git add proj5-ml/
git commit -m "p5: ..."
git push -u origin proj5
gh pr create --base main --head proj5
```

## Môi trường (conda)

Cả nhóm dùng chung một môi trường `cs188` với Python 3.10:

```bash
conda create -n cs188 python=3.10 -y
conda activate cs188
pip install "numpy<2.0" matplotlib
pip install torch --index-url https://download.pytorch.org/whl/cpu   # PyTorch bản CPU (cần cho Project 5)
```

Kiểm tra (Project 5):

```bash
cd proj5-ml
python autograder.py --check-dependencies
```

Chạy autograder cho từng project:

```bash
cd projX-...
python autograder.py              # chấm tất cả câu
python autograder.py -q q1        # chấm một câu
```
