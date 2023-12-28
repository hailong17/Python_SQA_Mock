# Python_SQA_Mock
# Yêu cầu đề bài là viết một đoạn mã Python để tự động kết nối SSH tới Raspberry Pi (Raspi) và thực hiện một số lệnh cơ bản trên Raspi. Để thực hiện điều này, chúng ta cần sử dụng thư viện Paramiko trong Python để thực hiện kết nối SSH và gửi các lệnh tới Raspi.

1. Import thư viện Paramiko: Đầu tiên, chúng ta cần import thư viện Paramiko để có thể sử dụng các lớp và phương thức liên quan đến kết nối SSH.

2. Xác định thông tin kết nối SSH: Chúng ta cần xác định địa chỉ IP của Raspberry Pi (raspi_ip_address), cổng mặc định (port), tên người dùng SSH trên Raspi (username), và mật khẩu SSH tương ứng (password).

3. Tạo đối tượng SSHClient: Sử dụng lớp SSHClient từ thư viện Paramiko để tạo một đối tượng SSHClient.

4. Thiết lập chính sách chấp nhận khóa host: Sử dụng phương thức set_missing_host_key_policy() trên đối tượng SSHClient để tự động chấp nhận khóa host không xác định.

5. Kết nối SSH đến Raspi: Sử dụng phương thức connect() trên đối tượng SSHClient để thực hiện kết nối SSH tới Raspberry Pi với thông tin xác thực tương ứng.

6. Thực hiện các lệnh cơ bản trên Raspi: Sử dụng phương thức exec_command() trên đối tượng SSHClient để gửi các lệnh cần thực hiện trên Raspi. Ví dụ: ls để liệt kê thư mục, pwd để hiển thị thư mục làm việc hiện tại.

7. Nhận kết quả trả về: Sử dụng các luồng (stdin, stdout, stderr) từ phương thức exec_command() để nhận kết quả trả về từ lệnh được thực thi trên Raspi.

8. Đóng kết nối SSH: Sử dụng phương thức close() trên đối tượng SSHClient để đóng kết nối SSH sau khi hoàn thành các lệnh.

# Implementation

        +---------------------+
        |      Local Machine   |
        +---------------------+
                 | (1) SSH Connection
                 |
        +---------------------+
        |     SSH Client      |
        +---------------------+
                 |
                 | (2) SSH Connection
                 |
        +---------------------+
        |       Raspi         |
        |     (SSH Server)    |
        +---------------------+

Mô hình này mô tả các thành phần và quy trình chi tiết như sau:

Local Machine: Đây là máy tính từ nơi bạn muốn kết nối và điều khiển Raspi. Đây có thể là máy tính cá nhân, máy tính xách tay hoặc bất kỳ thiết bị nào có khả năng thực thi mã Python.

SSH Client: Đây là phần mềm SSH client được chạy trên Local Machine. Trong đoạn mã Python, chúng ta sử dụng thư viện Paramiko để tạo SSH client và thực hiện kết nối SSH tới Raspi.

Raspi: Đây là Raspberry Pi, một thiết bị nhỏ gọn và mạnh mẽ chạy hệ điều hành Linux. Raspberry Pi cài đặt và chạy SSH Server để chấp nhận kết nối từ SSH Client.

Quy trình hoạt động:

SSH Client trên Local Machine tạo kết nối SSH đến Raspi bằng cách sử dụng mã Python và thư viện Paramiko. Quá trình này bao gồm việc xác thực và mã hóa thông tin giao tiếp.

Khi kết nối SSH được thiết lập, SSH Client trên Local Machine có thể gửi các lệnh và yêu cầu tới Raspi thông qua kết nối SSH. Các lệnh này được gửi dưới dạng chuỗi ký tự qua kết nối SSH.

SSH Server trên Raspi nhận các yêu cầu từ SSH Client thông qua kết nối SSH và thực thi các lệnh tương ứng trên Raspi. Kết quả của các lệnh được trả về dưới dạng chuỗi ký tự.

Kết quả từ các lệnh được trả về từ Raspi được chuyển tiếp từ SSH Server trên Raspi qua kết nối SSH đến SSH Client trên Local Machine.

SSH Client trên Local Machine nhận kết quả từ Raspi thông qua kết nối SSH và xử lý kết quả để hiển thị hoặc sử dụng theo mong muốn.

Sau khi hoàn thành công việc, kết nối SSH giữa SSH Client và SSH Server được đóng.
