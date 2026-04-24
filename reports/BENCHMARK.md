# Benchmark Report - Multi-Memory Agent

| # | Scenario | No-memory result | With-memory result | Pass? |
|---|----------|------------------|---------------------|-------|
| 1 | Recall User Name | "Xin lỗi, tôi không biết tên bạn là gì. Bạn có thể cho tôi biết không?" | "Tên bạn là Linh. Rất vui được gặp lại bạn!" | Pass |
| 2 | Allergy Conflict Update | "Bạn có thể uống trà sữa trân châu hoặc trà sữa đậu nành nếu thích." (Không biết dị ứng đậu nành mới) | "Vì bạn dị ứng đậu nành (thay cho sữa bò), bạn không nên uống sữa đậu nành. Hãy thử trà trái cây." | Pass |
| 3 | Episodic Recall | "Tôi không có thông tin về lần debug trước đó của chúng ta." | "Trong lần trước, chúng ta đã sửa lỗi 404 bằng cách sử dụng docker service name chính xác." | Pass |
| 4 | Semantic Knowledge Retrieval | "LangGraph là một thư viện để xây dựng graph..." (Thông tin chung) | "LangGraph là thư viện xây dựng ứng dụng multi-agent có trạng thái (stateful) với LLM." | Pass |
| 5 | Long Conversation Context | "Bạn đã hỏi về lịch sử AI ở câu đầu tiên." | "Câu hỏi đầu tiên của bạn là 'Chào bạn, mình tên là Linh' và sau đó bạn hỏi về lịch sử AI." | Pass |
| 6 | Preference Storage | "Tôi không nhớ bạn thích tông màu nào." | "Bạn thích tông màu tối cho website, vì vậy tôi gợi ý bảng màu Navy và Charcoal." | Pass |
| 7 | Work Outcome Recall | "Tôi có thể viết code cho bạn ngay bây giờ." | "Chúng ta đã viết xong đoạn code Python in ra 'Hello' ở lượt trước." | Pass |
| 8 | Technical Knowledge Retrieval | "Để sửa lỗi 404, hãy kiểm tra link..." | "Theo kiến thức của tôi, bạn nên kiểm tra xem route đã được định nghĩa trong Router chưa." | Pass |
| 9 | Complex Profile | "Tôi không biết bạn làm nghề gì." | "Bạn là kỹ sư phần mềm sống ở Hà Nội, vì vậy công việc của bạn thường là lập trình." | Pass |
| 10 | Task Progress Tracking | "Chúng ta đang trò chuyện bình thường." | "Chúng ta đang lên kế hoạch du lịch Đà Nẵng 3 ngày và vừa thảo luận về Ngày 1." | Pass |
