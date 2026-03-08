# Agency Report Format Skill Kit

English version: [README.md](README.md)

Repo này mô tả một skill cho Agent AI dùng để tạo DOCX bám sát form cơ quan từ bộ artifact tham chiếu đã được duyệt. Trọng tâm của skill không phải là thay placeholder, mà là đọc đúng cấu trúc của DOCX, PDF, và khi có thể là XML, rồi biến chúng thành một canonical format specification, một execution plan, và một pipeline sinh DOCX có kiểm chứng.

## Project Overview

Đây là repo mô tả một bài toán report generation có format fidelity cao.

Bài toán không dừng ở việc tính số liệu hay đổ dữ liệu vào một mẫu Word. Bài toán thật là tái tạo đúng artifact cuối cùng khi báo cáo có:

- bảng động thay đổi số dòng
- header nhiều tầng
- merged cells theo chiều ngang hoặc dọc
- total rows và note rows bắt buộc
- typography, spacing, page flow, và các ràng buộc Word/PDF cần giữ nguyên

Vì vậy, mail merge hoặc placeholder replacement là chưa đủ. Chúng có thể điền nội dung vào vị trí cố định, nhưng không đủ để tái tạo đúng table schema, merge map, total rows, note rows, hoặc hành vi layout của DOCX và PDF ở các section nhạy cảm.

Repo này chuẩn hóa cách để Agent AI xử lý đúng lớp bài toán đó.

## Human Input Boundary

Vai trò của con người trong skill này được giới hạn rõ ràng. Con người chỉ chuẩn bị các artifact tham chiếu sau:

1. DOCX mẫu đã duyệt
2. PDF được xuất từ DOCX đó
3. nếu có thể, thêm DOCX đã giải nén hoặc các XML thành phần

Từ đó trở đi, trọng tâm của repo là mô tả Agent AI phải làm gì với các artifact này.

## Agent Skill Flow

Skill này yêu cầu Agent AI vận hành theo chuỗi sau:

1. Đọc DOCX chuẩn để lấy cấu trúc nhìn thấy được: section order, heading hierarchy, table inventory, total rows, note rows, fixed wording.
2. Đọc PDF tham chiếu để hiểu chân lý hiển thị cuối: page breaks, page flow, spacing drift, width drift, visual parity.
3. Đọc DOCX XML đã giải nén để lấy cấu trúc Word-specific: grid structure, `w:gridSpan`, `w:vMerge`, header signatures, table boundaries.
4. Hợp nhất các fact vừa trích thành một canonical format specification.
5. Từ specification, lập execution plan và fix-layer map: data, template, post-process, XML, validation.
6. Dựng canonical report model và render DOCX vòng đầu bằng template.
7. Post-process các vùng nhạy cảm như dynamic tables, total rows, note rows, và merge behavior.
8. So DOCX sinh ra với DOCX/XML tham chiếu, đồng thời so PDF sinh ra với PDF tham chiếu ở các trang hoặc vùng nhạy cảm.
9. Nếu có mismatch, quay lại đúng fix layer thay vì sửa mò.
10. Xuất ra gói kết quả cuối gồm DOCX, specification, mismatch summary, và acceptance status.

## Technical Pipeline

Pipeline kỹ thuật mà repo này mô tả có thể tóm gọn thành 6 lớp:

1. Artifact ingestion  
   Agent AI nạp DOCX chuẩn, PDF chuẩn, và nếu có thì DOCX đã giải nén hoặc XML.

2. Structure extraction  
   Agent AI trích các structural facts: heading candidates, section order, table inventory, header rows, row groups, merge markers, style clues.

3. Layout interpretation  
   Agent AI đọc PDF để hiểu layout cuối, sau đó đối chiếu với DOCX và XML để phân biệt phần nào là visual rule, phần nào là Word structure rule.

4. Intermediate planning  
   Agent AI viết canonical format specification, xác định generation path, rồi tạo execution plan và fix-layer map.

5. Document generation  
   Agent AI render một DOCX vòng đầu từ template và canonical report model, sau đó patch các vùng nhạy cảm bằng post-process hoặc XML-level handling.

6. Validation and refinement  
   Agent AI kiểm structural parity, visual parity, acceptance status, rồi lặp lại đúng layer cho tới khi DOCX đủ chuẩn để review hoặc phát hành.

Đầu ra cuối cùng mà skill hướng tới là một file DOCX đủ sát form cơ quan, kèm theo các artifact giải thích tại sao output đó được xem là chấp nhận được.

## Core Libraries / Technical Components

Các thư viện và thành phần kỹ thuật phù hợp với repo này phải bám sát những gì hiện có trong script và source project gốc:

- `zipfile`  
  Dùng để mở `.docx` như gói OpenXML và đọc trực tiếp các XML thành phần.
- `xml.etree.ElementTree`  
  Dùng để parse `document.xml`, `styles.xml`, `numbering.xml`, và trích structural facts.
- `lxml`  
  Phù hợp khi cần XML inspection sâu hơn hoặc cần thao tác XML linh hoạt hơn chuẩn thư viện mặc định.
- `PyMuPDF` qua `fitz`  
  Dùng để đọc PDF, lấy page clues, render page images, và phục vụ visual review.
- `docxtpl`  
  Dùng để render DOCX vòng đầu từ template và context/model đã chuẩn hóa.
- `python-docx`  
  Dùng để post-process bảng, sửa total rows, note rows, merge behavior, và các phần Word structure nhạy cảm.
- `docx2pdf`  
  Dùng khi pipeline cần xuất PDF từ DOCX để so với PDF chuẩn.

Repo này không giả định một thư viện đơn lẻ làm được toàn bộ pipeline. Cách tiếp cận đúng là tách rõ lớp đọc artifact, lớp render, lớp post-process, và lớp validation.

## Repository Structure

Các thành phần cốt lõi trong repo chia sẻ này là:

- [.github/skills/report-form-reconstruction/SKILL.md](.github/skills/report-form-reconstruction/SKILL.md)  
  Định nghĩa skill, mục tiêu, workflow bắt buộc, anti-pattern, và deliverables của Agent AI.
- [.github/instructions/report-form-reconstruction.instructions.md](.github/instructions/report-form-reconstruction.instructions.md)  
  Bổ sung rule vận hành cho AI agent ở mức repository.
- [copilot-instructions.md](copilot-instructions.md)  
  Tập luật nền cho AI khi làm việc với bài toán report format chặt.
- [scripts/extract_format_spec.py](scripts/extract_format_spec.py)  
  Script mẫu để đọc DOCX hoặc XML và tạo draft canonical format specification.
- [artifacts/example-format-spec-VN.md](artifacts/example-format-spec-VN.md)  
  Ví dụ đầu ra trung gian mà Agent AI nên tạo ra trước khi sửa code hoặc render chính thức.
- [docs/how-we-read-the-approved-word-form-VN.md](docs/how-we-read-the-approved-word-form-VN.md)  
  Mô tả kỹ thuật cách đọc DOCX, XML, và PDF như source of truth nhiều lớp.
- [docs/methodology-VN.md](docs/methodology-VN.md)  
  Mô tả method, fix-layer thinking, và failure modes của bài toán.
- [docs/reference-artifact-ingestion-VN.md](docs/reference-artifact-ingestion-VN.md)  
  Giải thích thứ tự ưu tiên của DOCX, PDF, XML, screenshot, và verbal notes.

Các thành phần phụ trợ là:

- [templates/report-profile.template-VN.md](templates/report-profile.template-VN.md)  
  Khung để Agent AI draft hồ sơ report của một case cụ thể.
- [templates/artifact-package-for-ai.template-VN.md](templates/artifact-package-for-ai.template-VN.md)  
  Khung để Agent AI gom artifact bundle đầu vào.
- [templates/acceptance-checklist.template-VN.md](templates/acceptance-checklist.template-VN.md)  
  Khung để Agent AI draft acceptance checklist.
- [docs/how-to-use-with-ai-VN.md](docs/how-to-use-with-ai-VN.md)  
  Hướng dẫn cách đưa repo và artifact cho Agent AI.
- [docs/redaction-checklist-VN.md](docs/redaction-checklist-VN.md)  
  Hướng dẫn làm sạch dữ liệu trước khi public.
- [docs/publish-to-github-VN.md](docs/publish-to-github-VN.md)  
  Hướng dẫn public repo sau khi đã redaction.

## What This Repo Shares

Repo này chia sẻ các thành phần sau:

- cách Agent AI đọc DOCX, PDF, và XML như bộ source of truth nhiều lớp
- cách trích structural facts từ artifact tham chiếu
- cách biến structural facts thành canonical format specification
- cách dùng specification để lập plan trung gian và chọn đúng fix layer
- cách render, post-process, validate, và refine một DOCX cho tới khi đủ chuẩn format
- cách đóng gói toàn bộ logic trên thành một skill có thể tái sử dụng

## Scope and Non-Goals

Repo này không nhằm làm những việc sau:

- không phải universal report generator cho mọi loại tài liệu
- không phải mail merge template đơn giản
- không phải hướng dẫn chỉnh tay bằng Microsoft Word
- không phải bộ code nghiệp vụ đầy đủ cho từng đơn vị hoặc từng biểu mẫu thật
- không hứa tái tạo đúng mọi loại layout chỉ từ screenshot hoặc mô tả bằng lời

Phạm vi của repo là chuẩn hóa một skill cho Agent AI dùng để đi từ artifact tham chiếu sang DOCX có format fidelity cao, theo một pipeline rõ ràng và có thể kiểm chứng.
