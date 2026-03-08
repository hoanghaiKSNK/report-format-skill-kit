# Cách Đưa Repo Lên GitHub

Thư mục này đã được tổ chức sẵn theo kiểu một public repository độc lập.

## Trước Khi Push

1. Đọc lại [redaction-checklist-VN.md](redaction-checklist-VN.md).
2. Thay mọi placeholder cần kể lại câu chuyện hoặc định vị riêng của bạn.
3. Quyết định xem có giữ MIT License tại [LICENSE](../LICENSE) hay không.

## Tên Repo Gợi Ý

- report-format-skill-kit
- agency-report-reconstruction-skill
- ai-report-format-playbook

## Lệnh Gợi Ý

Chạy các lệnh này từ root của repository sau khi bạn tạo repo mới trên GitHub:

```powershell
Set-Location report-format-skill-kit
git add .
git commit -m "Initial public skill kit"
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

## Nếu Dùng GitHub CLI

Nếu máy đã cài `gh` và đã đăng nhập, bạn có thể làm như sau:

```powershell
Set-Location report-format-skill-kit
git add .
git commit -m "Initial public skill kit"
gh repo create report-format-skill-kit --public --source . --remote origin --push
```

## Commit Message Gợi Ý Cho Lần Đầu

`Initial public skill kit for strict report-format reconstruction`