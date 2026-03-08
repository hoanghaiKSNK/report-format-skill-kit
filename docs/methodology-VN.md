# Phương Pháp Tiếp Cận

Tài liệu này chỉ giữ phần decision model của skill.

## Mẫu Failure Mode

Các lỗi thường gặp trong bài toán report format chặt là:

- dữ liệu đúng nhưng sai thứ tự mục
- giá trị đúng nhưng sai cấu trúc bảng
- bảng đúng số liệu nhưng sai merge cell
- thiếu note rows hoặc total rows bắt buộc
- preview đúng nhưng DOCX export sai
- DOCX đúng nhưng PDF conversion lệch

## Canonical Format Specification Phải Chứa Gì

Trước khi generate, Agent AI phải viết ra tối thiểu:

- section order và heading hierarchy
- table inventory
- table schema và header structure
- vertical merge map và horizontal merge map
- mandatory total rows
- mandatory note rows hoặc footnotes
- fixed wording phải giữ nguyên
- typography, spacing, và page rules quan trọng

## Canonical Report Model Phải Chứa Gì

Format specification không giống report model.

- specification mô tả form yêu cầu gì
- report model mô tả report sinh ra chứa gì

Report model nên mô tả ít nhất:

- summary fields
- repeated sections
- table rows
- total rows
- note rows
- grouping và merge semantics

## Fix-Layer Decision Table

| Triệu chứng | Layer nên sửa |
| --- | --- |
| Sai giá trị | data mapping hoặc report model |
| Thiếu text biến | template binding |
| Sai thứ tự mục | template hoặc report model |
| Sai static layout | template |
| Thiếu total row bắt buộc | report model hoặc template |
| Sai wording của note row | template hoặc post-process |
| Sai merge row động | post-process |
| Sai Word structure khó giải thích | XML inspection |

## Validation Contract

Validation tối thiểu nên kiểm:

- section order
- heading
- table schema
- merged cells
- total rows và note rows
- font hoặc emphasis nếu có ý nghĩa nghiệm thu
- alignment, spacing, width nếu có ý nghĩa nghiệm thu
- page break hoặc overflow behavior
- parity sau conversion nếu PDF cũng là deliverable

## Nguyên Tắc Vận Hành

- không dùng preview làm bằng chứng DOCX đã đúng
- không yêu cầu Agent AI bắt chước file mẫu mà không viết specification trước
- không sửa mò nhiều layer cùng lúc khi chưa phân loại mismatch
- không trộn lẫn lỗi data với lỗi format