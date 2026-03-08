# Cách Đưa Artifact Tham Chiếu Cho AI

Tài liệu này chỉ trả lời một câu hỏi: artifact nào nên đưa cho Agent AI và mỗi loại dùng để đọc phần nào của format.

## Thứ Tự Ưu Tiên

1. DOCX chuẩn đã duyệt
2. PDF được xuất từ DOCX đó
3. DOCX đã giải nén hoặc các XML thành phần
4. structural notes đã redacted
5. screenshot hoặc side-by-side review images
6. mô tả bằng lời

Càng xuống cuối danh sách, Agent AI càng phải đoán nhiều hơn.

## Mỗi Artifact Dùng Để Đọc Gì

- DOCX chuẩn đã duyệt  
	Dùng để đọc section order, heading, bảng nhìn thấy được, total rows, note rows, và wording cố định.

- PDF tham chiếu  
	Dùng để đọc page breaks, spacing drift, width drift, overflow, và visual parity cuối.

- DOCX XML đã giải nén  
	Dùng để đọc grid structure, vertical merge, horizontal merge, và các chi tiết Word-specific.

- Structural notes  
	Dùng để làm rõ các ràng buộc mà artifact khó hiện hết bằng mắt thường.

- Screenshot  
	Dùng để chỉ ra vùng lệch rõ ràng, không nên dùng làm source of truth chính.

- Mô tả bằng lời  
	Chỉ nên dùng như ngữ cảnh phụ khi không thể chia sẻ artifact tốt hơn.

## Gói Tối Thiểu Khuyến Nghị

Nếu có thể, hãy luôn đưa cùng lúc:

- DOCX chuẩn đã duyệt
- PDF được xuất từ DOCX đó
- DOCX đã giải nén hoặc XML nếu merge behavior quan trọng

## Sau Khi Đọc Artifact, Agent AI Phải Viết Ra Gì

- section order
- heading hierarchy
- table inventory
- table schema
- merge map
- mandatory total rows
- mandatory note rows
- typography và spacing rules
- page rules

Nếu Agent AI chưa viết ra được các mục trên, nghĩa là nó chưa hiểu đủ source of truth.