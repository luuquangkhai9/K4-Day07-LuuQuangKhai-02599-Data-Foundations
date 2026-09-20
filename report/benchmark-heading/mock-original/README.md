# Kết quả benchmark Heading/Section

Đã chạy đúng 5 câu trong `REPORT_NHOM (1).md` trên 10 tài liệu,
164 chunk, mục tiêu 800 ký tự, top-k=3. Backend thực tế là mock vì
`EMBEDDING_PROVIDER` chưa được cấu hình. Không gọi API bằng key trong `.env`.

Q1/Q4 lọc buyer, Q2/Q3 lọc seller, Q5 không lọc. Có lưu thêm kết quả không
lọc của từng câu để đối chiếu trong [results.json](results.json).
Nội dung đầy đủ top-3: [retrieval.md](retrieval.md).

## Đối chiếu thủ công nội dung top-3

| Câu | Score top-1 | Nhận xét |
| --- | ---: | --- |
| Q1 | 0.251173 | Có một đoạn về danh mục hạn chế trả hàng, nhưng thiếu đối tượng COM, hạn mức 15 lần và điều kiện của gói VIP |
| Q2 | 0.193216 | Đúng audience seller nhưng thiếu mục 5 và thời hạn phản hồi 02 ngày lịch |
| Q3 | 0.244134 | Đúng audience seller nhưng không lấy được quy định chi phí tại mục 7 |
| Q4 | 0.300411 | Thiếu mục 8.1/8.2 so sánh hoàn phí Mall và ngoài Mall |
| Q5 | 0.335684 | Không lấy được mức tối thiểu 50% và lựa chọn xử lý khi không đồng ý |

**0/5 câu có đủ bằng chứng trong top-3 để trả lời toàn bộ gold answer.**
Đây không phải điểm rubric 0/10: chưa chạy LLM sinh câu trả lời, không tự điền
điểm agent. Mock dùng hash xác định, không biểu diễn ngữ nghĩa; kết quả không
chứng minh Heading/Section kém hơn các chiến lược dùng embedding thật.

## Các vấn đề cần xử lý trước lượt tiếp theo

- Q5: phần thao tác tiếp tục trao đổi/chọn trả hàng trong gold cần kiểm tra lại
  độ bao phủ của corpus hiện tại. Bài hướng dẫn trả lời đề xuất hoàn tiền đã bị
  loại khỏi 10 tài liệu. Mục 9.5 có mức 50% nhưng không tự cung cấp đầy đủ thao tác
  nói trên. Giữ nguyên câu hỏi/đáp án nhóm trong lượt chạy này, không tự đổi.
- Cấu trúc nguồn không đồng đều: mục 9.1 được đánh dấu `###`, trong khi 9.2–9.6
  là văn bản thường. Chunker hiện có thể gắn tiêu đề 9.1 cho nội dung 9.5.
  Quy tắc tách câu cũng có thể tách số `9.5.` thành đoạn riêng. Cần bổ sung nhận
  diện điều khoản đánh số và kiểm thử trước khi chạy lại; không sửa số liệu lượt
  này để che hạn chế đã quan sát.
- Chọn rõ embedding provider/model cho lượt đánh giá ngữ nghĩa; không suy ra
  rằng có API key nghĩa là đã dùng embedding thật. Chốt LLM để đánh giá câu trả
  lời của agent. Khi so sánh thành viên, giữ cùng backend và bộ câu hỏi.

## Chạy lại

Từ thư mục gốc dự án:

```powershell
.venv\Scripts\python.exe -X utf8 scripts/benchmark_heading.py
```

Script đọc provider từ môi trường/.env, không tự fallback khi API lỗi;
ghi đè `results.json` và `retrieval.md`. Bản nhận xét này chỉ áp dụng lượt mock
164 chunk nêu trên, cần cập nhật khi cấu hình hoặc thuật toán thay đổi.
