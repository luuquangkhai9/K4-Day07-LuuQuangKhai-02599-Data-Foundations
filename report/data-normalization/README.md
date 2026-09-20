# Chuẩn hóa dữ liệu Trả hàng/Hoàn tiền Shopee

Ngày thực hiện: 2026-09-20. Phạm vi: 14 tài liệu đã crawl trong
`data/return-refund-policy/`. Không crawl lại hoặc xác minh chính sách hiện hành
trên website trong bước này.

## Cập nhật: tách chính sách 77251 theo đối tượng

Đã bổ sung hai bản trích từ tài liệu 77251, giữ nguyên câu chữ và số điều khoản:

| File trong `data/return-refund-policy/` | Audience | Điều khoản giữ lại |
| --- | --- | --- |
| `shopee-chinh-sach-tra-hang-nguoi-mua.md` | `buyer` | 1, 2, 3, 4, 6, 8, 9, 10, 11, 12 |
| `shopee-chinh-sach-tra-hang-nguoi-ban.md` | `seller` | 1, 2, 3, 4, 5, 7, 9, 10, 11, 12 |

Bản người bán có riêng mục 5 (quyền phản hồi) và mục 7 (chi phí vận chuyển
hoàn trả); bản người mua có riêng mục 6 (yêu cầu sản phẩm hoàn trả) và mục 8
(chi phí của người mua). Các mục chung được giữ ở cả hai bản để bảo toàn phạm vi,
điều kiện, ngoại lệ và ngữ cảnh. Ví dụ mục 4 có ngoại lệ phí đối với người bán;
mục 9 có cả nghĩa vụ tài chính của người bán lẫn quy định hoàn tiền cho người mua.
`audience` biểu thị đối tượng sử dụng bản trích, không có nghĩa mọi câu chỉ nhắc
đến một phía. Các liên kết “ĐÂY” đã mất URL trong bản crawl vẫn chưa được phục hồi.

Hai file có cùng `source_url`, `retrieved_at`, `source_article_id: "77251"`,
`doc_id` riêng và metadata `source_sections` ghi các mục được trích.
`document_version: "2026-03-11"` lấy từ ngày hiệu lực tại mục 12.2;
ngày đăng 04/03/2026 vẫn được giữ trong nội dung. Không kiểm chứng lại website.

Đã thay dòng CSV của bản gốc bằng hai dòng cho hai bản trích. Hiện corpus có
**16 file: 15 `buyer`, 1 `seller`**, tương ứng 16 dòng CSV, từ 15 bài nguồn.
Vẫn cần chọn tập 5–10 tài liệu và thiết kế câu hỏi để kiểm chứng lợi ích của bộ lọc;
có đủ nhãn chưa tự động chứng minh bộ lọc cải thiện retrieval.

Bản gốc 77251 và CSV trước khi tách nằm trong
[shopee-77251-original.zip](shopee-77251-original.zip), ngoài thư mục `data/`.
Script thực hiện: [split_return_refund_policy.py](../../scripts/split_return_refund_policy.py).
Đã kiểm tra câu chữ, dấu câu và thứ tự các dòng của từng điều khoản được chọn
sau khi bỏ các dấu định dạng Markdown mới thêm.

Các phần dưới đây ghi lại lượt chuẩn hóa **14 tài liệu ban đầu**, trước khi thêm 77251.

## Kết quả

- Chuẩn hóa UTF-8, Unicode NFC, khoảng trắng và xuống dòng.
- Đổi tên 14 file và `doc_id` sang dạng `shopee-<ten-khong-dau>`.
- Giữ nguyên URL nguồn, ngày thu thập, `document_version: not-stated`
  và căn cứ sử dụng đã ghi trong CSV gốc.
- Bổ sung `audience: buyer`, `category: returns-policy`, `language: vi`.
  Các bài có nhắc đến người bán vẫn là hướng dẫn cho người mua; không vì thế
  mà gán nhãn `seller` hoặc `both`.
- Loại lời chào, tiêu đề lặp, hậu tố tên website, phần đánh giá bài viết,
  tên file video không có URL và ba dòng `1` rời cuối bài 189476.
- Định dạng tiêu đề mục, bước thực hiện và bullet; khôi phục các bảng có
  hàng/cột xác định được từ bản crawl ở bài 188931, 189473, 190242, 79467, 79508.
  Ô đầu cột trống trong bảng hoàn tiền/voucher tiếp tục nhóm của dòng trước.
- `sources.csv` có 14 dòng, khớp một-một với 14 file Markdown; đường dẫn dùng `/`.
- Giữ cả 14 tài liệu trong bước chuẩn hóa. Chưa chọn corpus 5–10 tài liệu để nộp.

## Bảo toàn và kiểm tra

- [Bản gốc ZIP](return-refund-policy-original.zip): 14 file và CSV trước chỉnh sửa,
  đã đối chiếu từng byte khi tạo; nằm ngoài `data/` để tránh nạp trùng vào RAG.
- [Ánh xạ tên file](filename-map.json): tên và `doc_id` trước/sau chuẩn hóa.
- [Script](../../scripts/normalize_return_refund.py): xử lý riêng bản crawl này,
  không gọi mạng; từ chối chạy khi thư mục đã chuẩn hóa hoặc đầu vào khác dự kiến.
- So sánh toàn bộ từ, số và dấu kiểm `✔` của nội dung giữ lại trước/sau định dạng.
  Chỉ bảng 189473 và 190242 cần đổi thứ tự token khi đưa ghi chú/header vào ô;
  hai bài này được kiểm tra số lần xuất hiện của từng token. Các bài còn lại
  được kiểm tra cả thứ tự token. Đây là kiểm tra bảo toàn bản crawl,
  không phải chứng nhận bản crawl đúng với website gốc.

## Những hạn chế còn lại của dữ liệu nguồn

| Bài | Phát hiện | Cách xử lý tiếp theo |
| --- | --- | --- |
| 79258 — Cẩm nang | Chỉ còn mục lục câu hỏi, không có đáp án hay URL liên kết | Đã gắn `document_type: navigation-index`; đề xuất loại khỏi corpus benchmark |
| 79467 — Bằng chứng | Mục 5 chỉ còn tiêu đề, thiếu hình minh họa | Không tự tạo nội dung thay ảnh; không dùng mục này làm gold answer |
| 79508 — Đóng gói | Hai dòng “Nếu bạn chọn hình thức…” chưa có phần hướng dẫn bằng ảnh đi kèm | Đối chiếu nguồn khi cần benchmark về nội dung ảnh |
| 164831 — SPayLater | Ví dụ hai trường hợp A/B và hóa đơn theo tháng đã bị dàn phẳng; thiếu hình minh họa | Giữ thứ tự văn bản, chưa suy đoán lại bảng ví dụ; đối chiếu nguồn trước khi dùng ví dụ làm gold answer |
| 189477 — Phương thức trả hàng | Bản crawl ghi “Bước 34” | Giữ nguyên; cần kiểm tra nguồn trước khi sửa số bước |
| 188931 và 190242 | Cách loại trừ ngày nghỉ khác nhau: bài 188931 loại thứ Bảy, Chủ Nhật và lễ/Tết; bài 190242 chỉ ghi chủ nhật và lễ/Tết | Không tự hợp nhất thành một quy định; tránh câu benchmark mơ hồ hoặc đối chiếu nguồn |
| Nhiều bài | Cụm “tại đây”, “hình bên dưới” không còn URL/ảnh tương ứng | Giữ phần văn bản đã có, không tự suy ra đích liên kết |

## Trước khi benchmark

1. Chọn 5–10 tài liệu có nội dung đủ để trả lời câu hỏi, ưu tiên loại bài mục lục.
2. Bổ sung nguồn thực sự dành cho người bán: hiện cả 14 bài là `buyer`, chưa đủ
   yêu cầu hai giá trị `audience` để so sánh lọc metadata.
3. Đối chiếu các phần thiếu ảnh/bảng hoặc khác nhau giữa nguồn nếu dùng chúng
   trong benchmark. Không dùng nội dung chưa có trong bản crawl làm đáp án chuẩn.
4. Khi nạp `Document`, đưa YAML front matter vào `metadata`, chỉ nhúng phần thân.
   Trình nạp phải xử lý hoặc loại `<br>` trong ô bảng như dấu xuống dòng.
