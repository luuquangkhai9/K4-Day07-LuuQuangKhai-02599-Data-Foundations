# Benchmark Heading/Section

Backend: `mock` / `mock embeddings fallback`.
Corpus: 10 tài liệu, 164 chunk; mục tiêu 800 ký tự, top-k=3.

Chưa chạy LLM sinh câu trả lời; chưa chấm điểm /10. Gold answer được sao chép nguyên văn từ bản nhóm, chưa tự sửa.
Các hash nguồn, cấu hình và top-3 không lọc để đối chiếu nằm trong `results.json`.

## Q1: Người mua nào đủ điều kiện Trả hàng COM, hạn mức của ShopeeVIP là bao nhiêu và trường hợp nào bị loại trừ?

Filter: `{"audience": "buyer"}`

Gold theo nhóm: Người mua hạng Vàng/Kim Cương hoặc dùng ShopeeVIP đủ điều kiện. ShopeeVIP có hạn mức 15 lần mỗi tháng; hạn mức không cộng dồn, quyền chấm dứt khi gói hết hiệu lực, và không áp dụng cho Shopee Mart hoặc nhóm sản phẩm/người bán bị loại trừ.

### Top 1 — score 0.251173

ID: `shopee-quy-dinh-chung-tra-hang-hoan-tien:heading:2`; audience: `buyer`

````text
# Những quy định chung về Trả hàng/Hoàn tiền của Shopee
## 1. Điều kiện Trả hàng/Hoàn tiền của Shopee
### ⚠️ Lưu ý:

Bạn vẫn có thể gửi yêu cầu Trả hàng/Hoàn tiền sau khi đã bấm nút ‘Đã nhận được hàng’ và vẫn còn trong thời hạn 15 ngày Trả hàng/Hoàn tiền quy định của Shopee

Yêu cầu Trả hàng/Hoàn tiền của bạn sẽ được phản hồi trong vòng 3-5 ngày làm việc*. Hãy theo dõi mục thông báo trên ứng dụng Shopee để nhanh chóng cập nhật tiến trình xử lý khiếu nại Trả hàng/Hoàn tiền

Với yêu cầu Trả hàng/Hoàn tiền cho các sản phẩm thuộc danh sách hạn chế trả hàng, tùy vào từng vấn đề khiếu nại của Người mua, Shopee sẽ chủ động xem xét để đưa ra quyết định cuối cùng.

*Các ngày trong tuần không bao gồm thứ Bảy, Chủ Nhật và các ngày nghỉ lễ/Tết theo quy định của pháp luật áp dụng
````

### Top 2 — score 0.248214

ID: `shopee-quy-trinh-xu-ly-tra-hang:heading:1`; audience: `buyer`

````text
# Quy trình Shopee xử lý yêu cầu Trả hàng/ Hoàn tiền
## 1. Nguyên tắc chung
### ⚠️ Lưu ý:

Bạn vui lòng thường xuyên theo dõi thông báo trên ứng dụng Shopee để nhanh chóng cập nhật tiến trình xử lý khiếu nại Trả hàng/Hoàn tiền cũng như kịp thời bổ sung các thông tin được yêu cầu từ Shopee (nếu có)
````

### Top 3 — score 0.230049

ID: `shopee-tra-hang-doi-y:heading:5`; audience: `buyer`

````text
# Những điều cần biết về Trả hàng do "Đổi ý/không còn nhu cầu"
## 3/ Những danh mục sản phẩm nào không được trả lại do "Đổi ý (Sản phẩm còn nguyên tem, nhãn mác, bao bì)"?
### Sức khỏe, Vệ sinh & Đồ cá nhân

- Dụng cụ Mẹ & Bé và Thiết bị Y tế cá nhân

- Trang phục lót, Đồ bơi & Vớ/Tất
````

## Q2: Người bán phải phản hồi yêu cầu Trả hàng/Hoàn tiền trong bao lâu, và điều gì xảy ra nếu không phản hồi đúng hạn?

Filter: `{"audience": "seller"}`

Gold theo nhóm: Người bán phải phản hồi trong 02 ngày lịch hoặc thời hạn khác do Shopee quy định. Nếu không phản hồi, Shopee hiểu người bán đồng ý với quyết định xử lý và không khiếu nại; Shopee có thể cân nhắc hoàn tiền mà không cần người mua trả hàng.

### Top 1 — score 0.193216

ID: `shopee-chinh-sach-tra-hang-nguoi-ban:heading:19`; audience: `seller`

````text
# Chính sách Trả hàng và Hoàn tiền — Người Bán
## 4. QUY ĐỊNH BỔ SUNG ĐỐI VỚI CÁC TRƯỜNG HỢP TRẢ HÀNG COM
### 4.3. Minh bạch thông tin

- b. Trong trường hợp nhận được khiếu nại của Người Bán về kết quả giải quyết yêu cầu Trả hàng COM trên hệ thống của Shopee, Shopee có quyền (mà không phải là nghĩa vụ) cung cấp các thông tin về (i) hạng thành viên, (ii) hạn mức Trả hàng COM còn lại của Người Mua cho Người Bán mà không cần phải thông báo cho Người Mua về việc cung cấp thông tin này. Tùy vào từng thời điểm và theo quyết định của riêng Shopee, việc cung cấp thông tin này có thể được thực hiện thông qua các nhãn (tag) gắn liền với tài khoản của Người Mua (nếu có) hoặc thông qua bộ phận có liên quan của Shopee.
````

### Top 2 — score 0.190558

ID: `shopee-chinh-sach-tra-hang-nguoi-ban:heading:31`; audience: `seller`

````text
# Chính sách Trả hàng và Hoàn tiền — Người Bán
## 9. HOÀN TIỀN ĐỐI VỚI SẢN PHẨM HOÀN TRẢ
### 9.1. Shopee sẽ chỉ hoàn tiền cho Người Mua thuộc một trong các trường hợp sau:

Shopee sẽ không chịu bất kỳ trách nhiệm nào có liên quan đến hoặc phát sinh từ việc Người Mua không tuân thủ các quy định liên quan dẫn đến việc chậm trễ hoặc không thể nhận tiền hoàn từ Shopee đối với Sản Phẩm Hoàn Trả.

9.5.

Đối với các trường hợp hoàn tiền ngay do Người Bán đề xuất, số tiền hoàn trả sẽ do hai Bên tự thỏa thuận với nhau nhưng không được thấp hơn 50% giá trị của Sản Phẩm Hoàn Trả.
````

### Top 3 — score 0.157963

ID: `shopee-chinh-sach-tra-hang-nguoi-ban:heading:1`; audience: `seller`

````text
# Chính sách Trả hàng và Hoàn tiền — Người Bán
## 1. ĐỐI TƯỢNG VÀ PHẠM VI ÁP DỤNG
### 1.2. Phạm Vi Áp Dụng

Chính Sách Trả Hàng và Hoàn Tiền này quy định về quyền và nghĩa vụ của Người Mua được yêu cầu trả hàng, hoàn tiền; cũng như quyền và nghĩa vụ của Shopee, Người Bán, đơn vị vận chuyển và/hoặc các bên có liên quan trong quá trình giải quyết yêu cầu của Người Mua.
````

## Q3: Theo chính sách dành cho người bán, trường hợp nào người bán chịu chi phí vận chuyển chiều hoàn trả và trường hợp nào không phải chịu?

Filter: `{"audience": "seller"}`

Gold theo nhóm: Người bán chịu phí với yêu cầu được Shopee chấp thuận không do lỗi người mua/đơn vị vận chuyển, đơn giao không thành công và ngoại lệ do Shopee quy định. Người bán không chịu phí với khiếu nại một phần, chưa nhận hàng, lỗi vận chuyển, hoàn tiền ngay không trả hàng, đơn tự vận chuyển giao không thành công hoặc hình thức người mua tự sắp xếp.

### Top 1 — score 0.244134

ID: `shopee-chinh-sach-tra-hang-nguoi-ban:heading:34`; audience: `seller`

````text
# Chính sách Trả hàng và Hoàn tiền — Người Bán
## 10. LIÊN LẠC GIỮA NGƯỜI BÁN VÀ NGƯỜI MUA

Shopee khuyến khích Người Mua chủ động liên hệ với Người Bán để thương lượng và giải quyết với nhau thông qua các kênh liên lạc được cung cấp trên hệ thống Shopee khi có bất cứ vấn đề nào phát sinh liên quan giao dịch mua Sản Phẩm. Lưu ý rằng việc sử dụng các kênh liên lạc bên ngoài hệ thống Shopee có thể sẽ có rủi ro cho Người Mua khi hệ thống Shopee không thể lưu lại bằng chứng của việc thương lượng này.
````

### Top 2 — score 0.238995

ID: `shopee-chinh-sach-tra-hang-nguoi-ban:heading:19`; audience: `seller`

````text
# Chính sách Trả hàng và Hoàn tiền — Người Bán
## 4. QUY ĐỊNH BỔ SUNG ĐỐI VỚI CÁC TRƯỜNG HỢP TRẢ HÀNG COM
### 4.3. Minh bạch thông tin

- b. Trong trường hợp nhận được khiếu nại của Người Bán về kết quả giải quyết yêu cầu Trả hàng COM trên hệ thống của Shopee, Shopee có quyền (mà không phải là nghĩa vụ) cung cấp các thông tin về (i) hạng thành viên, (ii) hạn mức Trả hàng COM còn lại của Người Mua cho Người Bán mà không cần phải thông báo cho Người Mua về việc cung cấp thông tin này. Tùy vào từng thời điểm và theo quyết định của riêng Shopee, việc cung cấp thông tin này có thể được thực hiện thông qua các nhãn (tag) gắn liền với tài khoản của Người Mua (nếu có) hoặc thông qua bộ phận có liên quan của Shopee.
````

### Top 3 — score 0.198758

ID: `shopee-chinh-sach-tra-hang-nguoi-ban:heading:31`; audience: `seller`

````text
# Chính sách Trả hàng và Hoàn tiền — Người Bán
## 9. HOÀN TIỀN ĐỐI VỚI SẢN PHẨM HOÀN TRẢ
### 9.1. Shopee sẽ chỉ hoàn tiền cho Người Mua thuộc một trong các trường hợp sau:

Shopee sẽ không chịu bất kỳ trách nhiệm nào có liên quan đến hoặc phát sinh từ việc Người Mua không tuân thủ các quy định liên quan dẫn đến việc chậm trễ hoặc không thể nhận tiền hoàn từ Shopee đối với Sản Phẩm Hoàn Trả.

9.5.

Đối với các trường hợp hoàn tiền ngay do Người Bán đề xuất, số tiền hoàn trả sẽ do hai Bên tự thỏa thuận với nhau nhưng không được thấp hơn 50% giá trị của Sản Phẩm Hoàn Trả.
````

## Q4: Nếu người mua tự sắp xếp trả hàng, chính sách hoàn chi phí khác nhau thế nào giữa sản phẩm Shopee Mall và sản phẩm không thuộc Shopee Mall?

Filter: `{"audience": "buyer"}`

Gold theo nhóm: Với Shopee Mall, Shopee hoàn đúng số phí vận chuyển đã trả qua Số Dư Tài Khoản Shopee trong 3–5 ngày làm việc khi yêu cầu được chấp nhận. Với sản phẩm không thuộc Shopee Mall, Shopee hỗ trợ một phần bằng Shopee Xu theo chính sách, cũng trong 3–5 ngày làm việc và phải đáp ứng điều kiện hỗ trợ.

### Top 1 — score 0.300411

ID: `shopee-chinh-sach-tra-hang-nguoi-mua:heading:30`; audience: `buyer`

````text
# Chính sách Trả hàng và Hoàn tiền — Người Mua
## 9. HOÀN TIỀN ĐỐI VỚI SẢN PHẨM HOÀN TRẢ
### 9.1. Shopee sẽ chỉ hoàn tiền cho Người Mua thuộc một trong các trường hợp sau:

Trường hợp Shopee nhận được khiếu nại từ Người Mua vì lý do Người Bán hoàn tiền thấp hơn 50% giá trị của Sản Phẩm Hoàn Trả thì Shopee, tại bất kỳ thời điểm nào, có quyền cấn trừ từ Số Dư Tài Khoản Shopee của Người Bán đó số tiền chênh lệch (được xác định bằng 100% giá trị Sản Phẩm Hoàn Trả trừ đi số tiền đã hoàn lại cho Người Mua) để thanh toán cho Người Mua mà không cần phải thông báo hay được sự đồng ý của Người Bán.

Quy định này nhằm ngăn chặn các hành vi trục lợi, đảm bảo tính minh bạch và công bằng của Chính Sách Trả Hàng và Hoàn Tiền của Shopee.
````

### Top 2 — score 0.272910

ID: `shopee-quy-trinh-xu-ly-tra-hang:heading:16`; audience: `buyer`

````text
# Quy trình Shopee xử lý yêu cầu Trả hàng/ Hoàn tiền
## 5. Câu hỏi thường gặp
### 5.4. Làm thế nào để theo dõi tình trạng vận chuyển đơn hàng hoàn trả về bạn, sau khi Shopee đã xem xét?

Sau khi bạn gửi hàng về để Shopee xem xét, nếu sản phẩm không đáp ứng các tiêu chí theo mục 4, Shopee rất tiếc sẽ chưa thể xử lý Hoàn tiền mà sẽ tiến hành hoàn trả hàng lại cho bạn.

Bạn có thể theo dõi tình trạng vận chuyển đơn hàng hoàn trả theo hướng dẫn dưới đây:

Đối với sản phẩm có nhãn Shopee Xử Lý: Bạn có thể theo dõi hành trình đơn hàng tại trang Chi tiết Trả hàng/ Hoàn tiền ngay trên ứng dụng Shopee theo hướng dẫn sau:

- Bước 1: Tại ứng dụng Shopee, chọn ‘Tôi’.

- Bước 2: Chọn ‘Xem lịch sử mua hàng’.

- Bước 3: Chọn thẻ ‘Trả hàng’.
````

### Top 3 — score 0.267181

ID: `shopee-chinh-sach-tra-hang-nguoi-mua:heading:22`; audience: `buyer`

````text
# Chính sách Trả hàng và Hoàn tiền — Người Mua
## 6. YÊU CẦU ĐỐI VỚI SẢN PHẨM HOÀN TRẢ

Để hạn chế các rủi ro phát sinh liên quan đến việc hoàn trả Sản Phẩm, Người Mua lưu ý cần phải đóng gói Sản Phẩm Hoàn Trả theo quy định về đóng gói hàng hóa được quy định tại Chính Sách Vận Chuyển Shopee và gửi trả Sản Phẩm bao gồm toàn bộ phụ kiện đi kèm, hóa đơn thuế GTGT, tem phiếu bảo hành (nếu có) và Sản Phẩm phải trong tình trạng nguyên vẹn như khi nhận hàng. Người Mua bắt buộc phải quay video và/hoặc chụp lại ảnh Sản Phẩm ngay khi nhận được và trong lúc đóng gói Sản Phẩm Hoàn Trả về để làm bằng chứng đối chiếu/khiếu nại về sau. Shopee sẽ thông báo cho Người Mua về việc phải cung cấp video hay ảnh chụp trong từng trường hợp cụ thể.
````

## Q5: Nếu người bán đề xuất Hoàn tiền ngay, mức hoàn tối thiểu là bao nhiêu và người mua có lựa chọn gì nếu không đồng ý?

Filter: `null`

Gold theo nhóm: Mức hoàn do hai bên thỏa thuận nhưng không thấp hơn 50% giá trị sản phẩm. Nếu đồng ý, người mua xác nhận để nhận hoàn tiền không cần trả hàng; nếu không đồng ý, người mua có thể tiếp tục trao đổi hoặc chọn trả hàng để yêu cầu hoàn toàn bộ theo quy trình.

### Top 1 — score 0.335684

ID: `shopee-chinh-sach-tra-hang-nguoi-ban:heading:27`; audience: `seller`

````text
# Chính sách Trả hàng và Hoàn tiền — Người Bán
## 7. TRÁCH NHIỆM VỀ CHI PHÍ VẬN CHUYỂN HOÀN TRẢ SẢN PHẨM CỦA NGƯỜI BÁN
### 7.2. Người Bán sẽ không phải chịu bất kỳ chi phí vận chuyển cho việc trả hàng chiều hoàn trả sản phẩm đối với:

đơn yêu cầu trả hàng/hoàn tiền được Shopee chấp nhận hoàn tiền ngay (không trả hàng) (theo quyết định riêng của Shopee),

đơn giao không thành công thuộc kênh Người bán tự vận chuyển, và

đơn yêu cầu trả hàng/hoàn tiền được Người mua lựa chọn hình thức "Tự sắp xếp" để trả hàng.

Vui lòng tham khảo chi tiết các thông tin về chi phí vận chuyển chiều hoàn trả sản phẩm của Người Bán tại ĐÂY.
````

### Top 2 — score 0.293651

ID: `shopee-thoi-gian-va-cach-kiem-tra-tien-hoan:heading:3`; audience: `buyer`

````text
# Thời gian nhận tiền hoàn và cách kiểm tra tiền hoàn

| Phương thức thanh toán | Tiền hoàn trả được gửi qua | Thời gian nhận được tiền hoàn sau khi Shopee chấp nhận hoàn tiền |
| --- | --- | --- |
| SPayLater | Mục Giao dịch trong SPayLater<br>*Lưu ý:<br>Nếu bạn gửi yêu cầu THHT sau khi đơn cập nhật trạng thái “Hoàn thành” - giao dịch trả góp đã được ghi nhận với ngân hàng:<br>-> Bạn vẫn cần trả góp cho đơn hàng này dù đã được chấp nhận Trả hàng/Hoàn tiền. Shopee sẽ hoàn trước 100% tiền hàng (tiền hoàn bao gồm số tiền gốc và không bao gồm phí chuyển đổi trả góp) vào tài khoản SPayLater của bạn, số tiền này sẽ được cấn trừ vào hóa đơn trả góp gần nhất. | 24 giờ |

Bảng 1: Phương thức hoàn tiền và thời gian hoàn tiền theo các phương thức thanh toán trên Shopee
````

### Top 3 — score 0.255876

ID: `shopee-tra-hang-doi-y:heading:4`; audience: `buyer`

````text
# Những điều cần biết về Trả hàng do "Đổi ý/không còn nhu cầu"
## 3/ Những danh mục sản phẩm nào không được trả lại do "Đổi ý (Sản phẩm còn nguyên tem, nhãn mác, bao bì)"?
### Thiết bị Điện tử & Công nghệ

(Có niêm phong / Kích hoạt / Bảo hành)

- Thiết bị di động, Máy tính

- Thiết bị Điện gia dụng & Giải trí gia đình

- Thiết bị Nhiếp ảnh, Camera & Trò chơi điện tử
````
