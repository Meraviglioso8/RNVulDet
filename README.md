# RNVulDet

This repo is a python implementation of our *RNVulDet* – a tool that incorporates taint analysis techniques to automatically unearth random number vulnerabilities and detect attack transactions.


## Overview
<div align=center><img width="880" height="280" src="./figs/overview.png"/></div>
*RNVulDet* comprises preprocessing and simulated execution. This Figure depicts the overall architecture of our proposed *RNVulDet*. In particular, RNVulDet engages in four main components to perform taint analysis, i.e., stack state examination, memory segmentation, storage key-value pair comparison, and transaction replay.

## Usage

```
python3 getSC.py
python3 main.py {BYTECODE_FILE} [-o {OUTPUT_FILE}]
```

## Dataset
Dataset\_1 contains 34 smart contracts reported to possess the random number bug.

Dataset\_2 includes a total of 214 smart contracts that do not have random number vulnerabilities.

Dataset\_3 consists of 4,617 potential victim contracts, 43,051 potential malicious contracts, and 49,951 suspicious transactions for experiments.

## Output
- Chạy dataset 1 (Dataset có lỗ hỏng bad randomness)
```
"is_reported": true - Đã tìm thấy một điều gì đó đáng chú ý trong hợp đồng thông minh, và đã được báo cáo. Điều này ngụ ý rằng có thể có một lỗ hổng hoặc vấn đề liên quan đến việc sử dụng số ngẫu nhiên.

"steps": 1 - Đây là số lượng bước hoặc hoạt động mà công cụ phải thực hiện để đưa ra kết luận của mình. Chỉ một bước ngụ ý rằng phân tích đó hoặc rất đơn giản hoặc là một kiểm tra cụ thể rất cụ thể đã được thực hiện.

"conditions": 3 - Số câu lệnh điều kiện hoặc điểm quyết định được liên quan trong phần của hợp đồng thông minh đang được phân tích. Trong bối cảnh của tính ngẫu nhiên, những điều kiện này có thể là nơi số ngẫu nhiên được sử dụng hoặc kiểm tra. Càng nhiều số lượng, logic điều kiện liên quan đến ngẫu nhiên càng phức tạp.

"call_values": 0 - Công cụ không tìm thấy bất kỳ trường hợp nào mà Ether hoặc token được chuyển giao trong phần mã mà nó phân tích. Điều này có liên quan bởi vì các giao dịch thường tương tác với các bộ sinh số ngẫu nhiên trong hợp đồng thông minh về trò chơi hoặc cờ bạc, nơi mà lỗ hổng có thể bị khai thác.

"to_addresses": 0 - Không có địa chỉ hợp đồng thông minh bên ngoài nào được gọi hoặc tương tác trong mã được phân tích. Điều này có thể liên quan trong việc đánh giá sự cô lập của quá trình sinh số ngẫu nhiên và sự dễ bị tác động từ bên ngoài.

"todo_keys": 1 -Có ít nhất một khía cạnh quan trọng hoặc hoạt động cần được chú ý hoặc phân tích thêm. Nó có thể ngụ ý một đường dẫn chưa được khám phá trong mã hoặc một khu vực tiềm ẩn nơi mà lỗ hổng liên quan đến ngẫu nhiên có thể tồn tại.
```
- Chạy dataset 2 (Dataset không có lỗ hỏng bad randomness)
```
"is_reported": false - Điều này cho thấy rằng công cụ không tìm thấy bất kỳ vấn đề hay lỗ hổng nào đáng chú ý liên quan đến việc sử dụng số ngẫu nhiên trong hợp đồng thông minh. Điều này chỉ ra rằng, ít nhất là theo khả năng và các kiểm tra của công cụ, hợp đồng thông minh không xuất hiện dấu hiệu của 'lỗ hổng ngẫu nhiên kém'.

"steps": 0 - Việc không có bất kỳ bước nào cho thấy rằng công cụ hoặc không cần thực hiện bất kỳ hoạt động nào để kết luận phân tích của mình, hoặc nó không tìm thấy bất kỳ đoạn mã nào liên quan để phân tích. Điều này có thể có nghĩa là hợp đồng thông minh không sử dụng số ngẫu nhiên theo cách mà công cụ được thiết kế để phân tích hoặc xem xét.

"conditions": 0 - Không có logic điều kiện liên quan đến ngẫu nhiên nào được phát hiện trong hợp đồng thông minh. Điều này có thể có nghĩa là hợp đồng hoặc không sử dụng số ngẫu nhiên, hoặc sử dụng chúng một cách đơn giản mà không có điều kiện phức tạp.

"call_values": 0 - Tương tự như kết quả trước, điều này cho thấy không có chuyển giao Ether hoặc token trong các phần của hợp đồng thông minh được phân tích bởi công cụ. Điều này càng hỗ trợ ý tưởng rằng các hoạt động của hợp đồng liên quan đến ngẫu nhiên (nếu có) không tương tác với chuyển giao giá trị.

"to_addresses": 0 - Công cụ không tìm thấy bất kỳ tương tác nào với các địa chỉ hợp đồng thông minh bên ngoài. Điều này ngụ ý rằng chức năng của hợp đồng, trong bối cảnh của ngẫu nhiên, là tự chứa và không phụ thuộc vào các nguồn bên ngoài.

"todo_keys": 0 - Không có khía cạnh hay hoạt động nào được đánh dấu cần thêm điều tra. Điều này có nghĩa là công cụ không xác định bất kỳ khu vực nào trong hợp đồng thông minh có thể cần thêm sự chú ý liên quan đến việc sử dụng số ngẫu nhiên.
```
