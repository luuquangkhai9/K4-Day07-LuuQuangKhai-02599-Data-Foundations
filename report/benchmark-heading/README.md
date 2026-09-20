# Benchmark Heading/Section với Gemini embedding

## Cấu hình và bằng chứng

Đã chạy thành công bằng **Gemini `gemini-embedding-001`**, không fallback sang mock.
Corpus gồm 10 tài liệu, 164 chunk từ `HeadingSectionChunker(800)`; 5 câu hỏi giữ
nguyên theo `REPORT_NHOM (1).md`; top-k=3. Q1/Q4 lọc buyer, Q2/Q3 lọc seller,
Q5 không lọc. Mỗi câu cũng được chạy không lọc để đối chiếu.

Giữ nguyên thuật toán và corpus của lượt mock để so sánh tác động của embedding.
Sử dụng lời gọi embed_content mặc định cho cả tài liệu và truy vấn, không đặt
`task_type` riêng. Điểm xếp hạng là cosine similarity, không phải xác suất đúng.
Chạy trong `.venv` Python 3.12 với SDK google-genai 2.24.0.

- [Kết quả đầy đủ JSON](results.json): cấu hình, thời gian UTC, hash nguồn, top-3 có/không lọc.
- [Nội dung các chunk truy xuất](retrieval.md).
- [Lượt mock đã lưu](mock-original/results.json).

API có trả 429 giữa lượt chạy; script chờ rồi thử lại thành công. Tổng 169 văn bản
được nhúng gồm 164 chunk và 5 câu hỏi. Embedding được lưu cache cục bộ theo model
và nội dung để tránh gọi lại; cache được loại khỏi Git. Không ghi API key vào log.

## Kết quả đối chiếu thủ công

| Câu | Score top-1 | Nội dung top-3 | Mức bao phủ gold answer |
| --- | ---: | --- | --- |
| Q1 | 0.872431 | Đúng phần đối tượng COM, hạn mức không cộng dồn và quyền hết hiệu lực | Một phần: thiếu con số 15 lần/tháng và các loại trừ như Shopee Mart |
| Q2 | 0.787446 | Có thời hạn 02 ngày lịch, thời điểm nhận thông báo và hệ quả không phản hồi | Một phần: thiếu câu ở mục 5 về cân nhắc hoàn tiền không cần trả hàng; mục 9.2 truy xuất được có điều kiện khác, không thể tự coi tương đương |
| Q3 | 0.832623 | Có đủ mục 7.1 và hai phần mục 7.2 | Đủ bằng chứng cho các trường hợp chịu/không chịu phí trong gold |
| Q4 | 0.862981 | Có mục 8.1 và cả hai chunk của mục 8.2 | Đủ: Mall hoàn phí qua Số Dư Tài Khoản Shopee; ngoài Mall hỗ trợ bằng Xu, điều kiện và thời gian |
| Q5 | 0.752323 | Có điều khoản 9.5 về mức tối thiểu 50%; top-1 và top-2 lặp nội dung giữa hai audience | Một phần: thiếu lựa chọn thao tác khi người mua không đồng ý |

**5/5 câu có ít nhất một đoạn liên quan trực tiếp trong top-3; 2/5 câu có đủ
bằng chứng cho toàn bộ gold answer.** Đây là đánh giá nội dung retrieval thủ công,
không phải điểm agent /10. Chưa gọi LLM sinh câu trả lời; `agent_answer` và
`rubric_score` vẫn là null. Không biến embedding model thành mô hình sinh văn bản.

Lượt mock trước có 0/5 câu đủ bằng chứng, lượt Gemini có 2/5 với cùng corpus và
chunking. Như vậy embedding ngữ nghĩa cải thiện việc tìm đúng điều khoản trong
thí nghiệm này; chưa đủ cơ sở kết luận chiến lược Heading/Section tốt hơn các
chiến lược khác khi chưa chạy chúng với cùng Gemini và cùng cấu hình đánh giá.

## Tác động của metadata filter

- **Q1:** không lọc có một chunk cùng nội dung COM ở cả buyer và seller chiếm hai
  vị trí. Lọc buyer loại bản lặp seller, bổ sung đoạn về không cộng dồn/hết hiệu
  lực, nhưng vẫn chưa đủ hạn mức và ngoại lệ.
- **Q2:** không lọc, top-1 là thời gian xử lý phía người mua (score 0.804774);
  điều khoản 02 ngày của người bán ở top-2. Lọc seller đưa điều khoản đúng lên
  top-1 và loại các đoạn buyer có thời hạn khác. Đây là bằng chứng rõ nhất về
  tác dụng lọc đúng đối tượng; không có nghĩa không lọc hoàn toàn mất đáp án.
- **Q3/Q4:** top-3 có và không lọc giống nhau; chưa thấy lợi ích bổ sung của lọc
  trong hai câu này.
- **Q5:** không lọc theo thiết kế nhóm; hai chunk gần trùng nhau làm giảm độ đa
  dạng bằng chứng trong top-3.

## Hạn chế và bước tiếp theo

1. Câu hỏi nhiều ý (Q1) cần nhiều đoạn. Mục tiêu 800 ký tự có thể tách hạn mức,
   đối tượng và ngoại lệ ra nhiều chunk; top-3 chưa đủ. Cần thử thay kích thước
   hoặc bổ sung chunk lân cận trong thí nghiệm riêng, không đổi ngầm lượt này.
2. Q2 cho thấy một điều khoản bị chia thành nhiều chunk: đã lấy thời hạn và hệ
   quả không phản hồi nhưng chưa lấy câu cuối về hoàn tiền không trả hàng.
3. Heading nguồn không đồng đều: mục 9.1 là heading, 9.2–9.6 là văn bản thường.
   Vì vậy chunk chứa 9.5 bị gắn đường dẫn 9.1; số `9.5.` cũng bị tách thành đoạn
   riêng. Cần cải thiện nhận diện điều khoản trước lượt thử thuật toán tiếp theo.
4. Gold Q5 cần được nhóm đối chiếu lại với corpus đã chọn: mục 9.5 nêu 50%, nhưng
   không nêu đủ thao tác tiếp tục trao đổi/chọn trả hàng. Bài hướng dẫn trả lời
   đề xuất đã bị loại khỏi corpus. Giữ nguyên gold nhóm trong báo cáo này; không
   tự thêm nguồn hoặc đổi câu hỏi để tăng điểm.
5. Muốn chấm rubric đầy đủ cần chọn LLM sinh câu trả lời, chạy trên chính context
   top-3 và đánh giá mức bám nguồn; không suy ra điểm trả lời chỉ từ cosine.

## Chạy lại

```powershell
$env:EMBEDDING_PROVIDER = 'gemini'
.venv\Scripts\python.exe -X utf8 scripts/benchmark_heading.py
```

API key được đọc từ `.env`; có thể đặt `GEMINI_EMBEDDING_MODEL` nếu cần.
Script không fallback khi API lỗi. Lệnh ghi đè `results.json`/`retrieval.md`;
nhận xét thủ công tại đây áp dụng lượt Gemini 164 chunk nêu trên.
