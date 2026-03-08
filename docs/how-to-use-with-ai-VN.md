# Cách Dùng Với AI

Tài liệu này chỉ mô tả ranh giới giao việc cho Agent AI.

## Input Tối Thiểu

Đưa cho Agent AI:

1. DOCX mẫu đã duyệt
2. PDF được xuất từ DOCX đó
3. nếu có thể, thêm DOCX đã giải nén hoặc XML
4. [../copilot-instructions.md](../copilot-instructions.md)
5. [../.github/skills/report-form-reconstruction/SKILL.md](../.github/skills/report-form-reconstruction/SKILL.md)

Các template trong `templates/` là tùy chọn. Agent AI có thể tự draft chúng nếu cần lưu lại report profile, artifact package, hoặc acceptance checklist.

## Agent AI Phải Làm Gì

Sau khi nhận input, Agent AI phải tự:

1. xác định source of truth
2. trích structural facts từ DOCX, PDF, và XML
3. viết canonical format specification
4. lập execution plan và fix-layer map
5. render DOCX vòng đầu
6. post-process các vùng nhạy cảm
7. validate lại output

Con người chủ yếu chỉ review output cuối.

## Prompt Gợi Ý

```text
Chúng tôi có một báo cáo phải khớp với biểu mẫu đã được duyệt.
Hãy dùng skill report-form-reconstruction.
Xem DOCX, PDF, và XML tham chiếu là source of truth.
Trước hết hãy trích section order, table schema, merge map, total rows, note rows, typography rules, và page rules.
Sau đó viết canonical format specification.
Tiếp theo hãy lập execution plan, chọn fix layer phù hợp, sinh DOCX, và tự kiểm lại output.
Không được giả định rằng preview đúng nghĩa là DOCX cũng đúng.
```

## Output Agent AI Nên Trả Về

Một lần chạy tốt nên trả về ít nhất:

- canonical format specification draft
- execution plan hoặc fix-layer map
- generated DOCX
- mismatch summary
- acceptance status

## Khi Áp Dụng Vào Repo Thật

Chỉ cần bổ sung các fact thật mà repo công khai này không thể chứa sẵn:

- tên artifact tham chiếu thật
- entry point generation path thật
- danh sách section hoặc bảng nhạy cảm
- ghi chú conversion behavior nếu DOCX và PDF đều là deliverable