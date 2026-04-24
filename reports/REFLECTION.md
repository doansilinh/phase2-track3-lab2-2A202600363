# Reflection - Multi-Memory Agent (Lab #17)

## Privacy & PII Risks
1.  **Sensitive Data Storage**: `LongTermMemory` và `EpisodicMemory` lưu trữ các sự thật cá nhân (tên, sở thích, dị ứng) và lịch sử hành vi. Dữ liệu này hiện lưu dưới dạng văn bản thuần túy trong thư mục `data/`, chưa được mã hóa.
2.  **Lack of TTL**: Hệ thống chưa có cơ chế tự động xóa dữ liệu cũ sau một khoảng thời gian (Time-To-Live).
3.  **Data Leakage**: Nếu dùng chung một file `long_term_memory.json` cho nhiều người dùng, thông tin của người này có thể bị rò rỉ sang người khác.

## Most Sensitive Memory Type
**Long-term Memory** là nhạy cảm nhất vì nó lưu trữ các sự thật có cấu trúc về người dùng, có thể bị khai thác để định danh hoặc xây dựng hồ sơ trái phép.

## Deletion & Consent
- **Consent (Quyền kiểm soát)**: Chúng ta đã triển khai lệnh `/memory off` để người dùng có thể chủ động ngừng việc ghi nhớ thông tin ngay lập tức. Đây là một bước tiến về mặt quyền riêng tư so với bản gốc.
- **Deletion**: Việc xóa hoàn toàn dữ liệu đòi hỏi phải làm sạch các file trong thư mục `data/`.

## Technical Improvements & Limitations
1.  **Auto-tagging (Cải tiến)**: Việc sử dụng LLM để tự động gắn thẻ (Tags) trong Semantic Memory giúp tăng cường khả năng truy xuất mà không cần người dùng thao tác thủ công.
2.  **Flexible Search (Cải tiến)**: Hệ thống tìm kiếm từ khóa đã được nâng cấp để hỗ trợ tìm kiếm cả trong nội dung và thẻ, cùng với cơ chế tính điểm (scoring) linh hoạt hơn.
3.  **Keyword Search Limitations**: Mặc dù đã cải tiến, nhưng so với các Vector Database thực thụ (FAISS, Chroma), việc tìm kiếm từ khóa vẫn có thể bỏ lỡ các ngữ cảnh đồng nghĩa.
4.  **Extraction Errors**: LLM có thể trích xuất sai sự thật từ câu nói của người dùng hoặc tạo ra các thẻ (tags) không liên quan.
5.  **Scaling**: Việc lưu trữ trong các file JSON trong thư mục `data/` chỉ phù hợp cho quy mô Lab. Thực tế cần dùng Redis hoặc PostgreSQL.

## Conclusion
Kiến trúc Multi-Memory đã giúp Agent trở nên "thông minh" và cá nhân hóa hơn rõ rệt. Các tính năng mới như Auto-tagging và Memory Toggle đã làm cho hệ thống trở nên hoàn thiện và thực tế hơn so với yêu cầu ban đầu của bài Lab.
