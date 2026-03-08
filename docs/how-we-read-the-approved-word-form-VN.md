# Cách Chúng Tôi Đọc File Word Mẫu Đã Duyệt

Tài liệu này mô tả implementation pattern đứng sau skill.

## Mô Hình Nhiều Lớp Artifact

Skill không đọc một file duy nhất. Nó đọc nhiều lớp source of truth:

1. DOCX chuẩn để lấy cấu trúc nhìn thấy được
2. template dẫn xuất từ DOCX đó để render vòng đầu
3. chính DOCX chuẩn để làm structural reference khi post-process
4. DOCX XML đã giải nén để validate structure
5. PDF chuẩn để review hiển thị cuối

## Trình Tự Kỹ Thuật

### 1. Đọc DOCX chuẩn

Agent AI dùng DOCX chuẩn để xác định section order, heading, bảng, total rows, note rows, và structural pattern lặp lại.

### 2. Render vòng đầu từ template

Agent AI render canonical report model vào một template đã gần với biểu mẫu chuẩn. Ở bước này mục tiêu là đúng data trên một cấu trúc gần đúng, chưa phải fidelity tuyệt đối.

### 3. Post-process với reference DOCX

Sau render, Agent AI mở song song DOCX sinh ra và DOCX chuẩn. Những section nhạy cảm được rebuild hoặc patch bằng chính cấu trúc của DOCX chuẩn.

Các fix thường gặp là:

- rebuild dynamic tables từ prototype row
- copy reference tail rows cho note rows hoặc footnotes
- thay total row bằng merge structure từ form chuẩn
- khôi phục vertical merge behavior cho bảng appendix có grouping

### 4. Validate bằng XML

Agent AI so generated DOCX với XML tham chiếu để kiểm:

- table count
- section count
- header-row signatures
- grid column counts
- maximum cell counts
- `w:vMerge`
- `w:gridSpan`

### 5. Review bằng PDF

Nếu PDF là deliverable, Agent AI so generated PDF với approved PDF để kiểm:

- page breaks
- spacing drift
- width drift
- paragraph flow
- visual parity ở vòng cuối

## Output Trung Gian Bắt Buộc

Trong quá trình trên, Agent AI phải viết ra:

- canonical format specification
- execution plan hoặc fix-layer map
- mismatch summary

Nếu thiếu các output trung gian này, pipeline rất dễ quay về kiểu sửa mò.