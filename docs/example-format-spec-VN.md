# Ví Dụ Canonical Format Specification

Đây là ví dụ ngắn về artifact trung gian mà Agent AI nên viết ra trước khi sửa code hoặc khẳng định output đã đạt format fidelity.

## Source Artifacts

- DOCX chuẩn đã duyệt: monthly-agency-report.docx
- PDF chuẩn: monthly-agency-report.pdf
- XML đã giải nén: word/document.xml, word/styles.xml

## Thứ Tự Các Mục

1. Tiêu đề trang đầu
2. Tóm tắt phạm vi báo cáo
3. Bảng thống kê chính
4. Bảng appendix theo nhóm
5. Ghi chú và khối chữ ký

## Quy Tắc Bảng

### Bảng thống kê chính

- Header có 2 tầng
- Cột đầu tiên là cột nhãn dòng cố định
- Dòng cuối là total row bắt buộc
- Ngay sau total row phải có một note row
- Không được đổi thứ tự các cột kháng sinh đã duyệt

### Bảng appendix theo nhóm

- Cột đầu tiên dùng vertical merge cho nhãn nhóm
- Số dòng động bên trong từng nhóm là hợp lệ
- Hành vi merge của nhãn nhóm phải giữ được sau khi xuất DOCX

## Quy Tắc Typography Và Phân Trang

- Heading phải giữ bold
- Chữ trong header bảng phải căn giữa
- Trước phần appendix phải có page break
- Khối chữ ký phải nằm ở trang cuối

## Điểm Kiểm Nhạy Cảm

- thứ tự mục
- wording của total row
- wording của note row
- vertical merge map ở bảng appendix
- page break trước appendix

## Gợi Ý Fix Layer

- Sai giá trị: report model hoặc data mapping
- Sai header tĩnh: template
- Sai merge động: post-process hoặc XML inspection
- Sai phân trang sau conversion: PDF validation và conversion layer