# Template Gói Artifact Giao Cho AI

Đưa file này cho AI để AI tự gom bộ artifact tối thiểu mà nó nên đọc trước khi đụng vào code. Bạn chỉ cần bổ sung đường dẫn hoặc fact còn thiếu.

## Mục Đích

- Gói artifact này phục vụ cho báo cáo hoặc deliverable nào?
- Vì sao format fidelity lại quan trọng trong trường hợp này?

## Artifact Bundle

- DOCX chuẩn đã duyệt:
- PDF được xuất từ DOCX đó:
- Folder DOCX đã giải nén:
- Structural notes do con người viết:
- Screenshot hoặc ảnh so sánh từng vùng:

## Thứ Tự Ưu Tiên Source Of Truth

Hãy ghi rõ thứ tự ưu tiên cho case này.

1. 
2. 
3. 

## Agent AI Phải Tạo Gì

- canonical format specification draft
- execution plan hoặc fix-layer map
- generated DOCX
- mismatch summary
- acceptance status

## Các Section Nhạy Cảm

- Section hoặc table 1:
- Section hoặc table 2:
- Section hoặc table 3:

## Rủi Ro Đã Biết

- Sai giá trị nhưng đúng cấu trúc:
- Đúng giá trị nhưng sai layout:
- Drift ở DOCX:
- Drift ở PDF:
- Drift liên quan merge:

## Prompt Gợi Ý

```text
Chúng tôi có một báo cáo phải khớp chính xác với biểu mẫu đã được duyệt.
Hãy xem các artifact trong gói này là source of truth.
Đọc DOCX, PDF, DOCX XML đã giải nén, và structural notes trước.
Liệt kê section order, table schema, merge map, total rows, note rows, typography rules, và page rules.
Viết canonical format specification draft trước khi đề xuất thay đổi code.
Sau đó xác định generation path hiện tại và phân loại từng fix vào data, template, post-process, hoặc XML handling.
```