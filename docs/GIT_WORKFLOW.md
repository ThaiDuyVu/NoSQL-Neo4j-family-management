# GIT WORKFLOW

```
feature/*
    ↓ PR
member/<name>
    ↓ PR
main
```

**Không push trực tiếp `main`.**

## Nhánh

| Thành viên | Nhánh cá nhân | Nhánh feature |
|------------|---------------|---------------|
| Vũ | `member/vu` | `feature/vu-person-crud`, `feature/vu-dashboard` |
| Sơn | `member/son` | `feature/son-relationship`, `feature/son-family-graph` |
| Đạt | `member/dat` | `feature/dat-kinship-search`, `feature/dat-kinship-resolver` |

## Khởi tạo (người lập repo làm một lần)
```bash
git init && git add . && git commit -m "chore: project skeleton"
git branch -M main
git remote add origin <repo-url> && git push -u origin main
git checkout -b member/vu   && git push -u origin member/vu
git checkout main
git checkout -b member/son  && git push -u origin member/son
git checkout main
git checkout -b member/dat  && git push -u origin member/dat
```
Trên GitHub/GitLab: bật **branch protection** cho `main` (bắt buộc PR + ít nhất 1 review).

## Quy trình mỗi feature (ví dụ Vũ)
```bash
git checkout member/vu && git pull
git checkout -b feature/vu-person-crud
# ... code, test ...
git add features/person tests/person
git commit -m "feat(person): implement create/update/delete"
git push -u origin feature/vu-person-crud
# Mở PR: feature/vu-person-crud -> member/vu
```
Khi một mốc hoàn thành và test pass: mở PR `member/vu -> main`, **một thành viên khác review**.

## Cập nhật từ main
```bash
git checkout member/vu
git fetch origin && git merge origin/main
```
Nên làm trước khi mở PR vào `main`.

## Commit message
`feat(person): ...`, `fix(relationship): ...`, `test(kinship): ...`, `docs: ...`, `chore: ...`
Scope = tên feature.

## Tránh conflict
- Chỉ sửa file trong domain của mình (xem `docs/MEMBER_*.md`).
- `app.py`: chỉ sửa block TAKE NOTE của mình.
- File shared (`core/*`, `shared/*`, `database/*`, `docker-compose.yml`, `requirements.txt`): sửa ít, commit riêng, nhắn nhóm trước. Thêm thư viện mới vào `requirements.txt` thì thêm ở **cuối file**.
- Không format lại cả file/không đổi tên hàng loạt trong file shared.

## Checklist PR
- [ ] Chỉ đụng file trong domain của mình (hoặc đã báo nhóm)
- [ ] `pytest tests/<domain>` pass
- [ ] Không có Cypher trong `page.py`; không import `repository` của feature khác
- [ ] Đã xóa `TODO` / `raise NotImplementedError` đối với phần đã làm
- [ ] Cập nhật README_<NAME>.md nếu đổi hành vi
