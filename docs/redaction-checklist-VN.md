# Checklist Redaction

Hãy dùng checklist này trước khi public phiên bản của bạn từ repository này.

## Những Gì Cần Xóa Hoặc Redact

- dữ liệu bệnh nhân hoặc dữ liệu khách hàng thật
- mã đơn vị, định danh, hoặc mã nội bộ thật
- biểu mẫu pháp lý hoặc biểu mẫu nội bộ mà bạn không được phép công bố
- đường dẫn mạng nội bộ
- hostname, username, token, hoặc API key nội bộ
- screenshot chứa thông tin nhạy cảm
- business logic độc quyền chưa được phép chia sẻ

## Những Gì Thường An Toàn Để Chia Sẻ

- mô tả workflow đã khái quát hóa
- field dictionary đã redacted
- sample row tổng hợp hoặc sample row giả lập
- sơ đồ kiến trúc
- acceptance checklist
- reusable AI skills và instructions

## Câu Hỏi Cần Tự Kiểm Tra Trước Khi Public

1. Có ai đó có thể dựng lại source material nhạy cảm chỉ từ repo này không?
2. Tên file, screenshot, hoặc ví dụ có chứa định danh nội bộ không?
3. Sau khi redact, instructions còn hữu ích hay không?
4. Repo public này đang tập trung vào phương pháp hay đang lộ ra implementation bí mật?