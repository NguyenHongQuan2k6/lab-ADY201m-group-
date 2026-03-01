import sys
import requests
from bs4 import BeautifulSoup

# --- SỬA LỖI CIRCULAR IMPORT ---
# Thay vì import mainpage, bạn khai báo link trực tiếp ở đây
url_get = 'https://www.nhaccuatui.com/chart/1-5-d58-2026' 
# -------------------------------

try:
    r = requests.get(url_get)

    # Kiểm tra kết nối thành công (200)
    if r.status_code == 200:
        r.encoding = 'UTF-8' # Đặt mã hóa để không lỗi font tiếng Việt
        information_page = r.text
        
        # Tên file mới muốn tạo
        ten_file_moi = 'information_web.txt'

        with open(ten_file_moi, 'w', encoding='utf-8') as f:
            # Lưu lại đầu ra mặc định (màn hình)
            man_hinh_goc = sys.stdout 
            
            # Chuyển hướng đầu ra vào file
            sys.stdout = f 
            
            # Ghi nội dung HTML vào file
            sys.stdout.write(information_page)
            
            # Trả lại đầu ra về màn hình
            sys.stdout = man_hinh_goc

        print(f"Thành công! Đã lưu mã nguồn trang web vào file '{ten_file_moi}'")
    
    else:
        print(f"Lỗi kết nối: Mã {r.status_code}")

except Exception as e:
    print(f"Có lỗi xảy ra: {e}")