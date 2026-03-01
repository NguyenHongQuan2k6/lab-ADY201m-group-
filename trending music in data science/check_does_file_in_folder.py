import os

# Đây là đường dẫn đến THƯ MỤC (Folder) chứa file của bạn
# Tôi đã cắt bỏ tên file ở cuối, chỉ giữ lại đường dẫn thư mục
duong_dan_folder = r"C:\Users\hongq\OneDrive\Desktop\Python\ADY201m\lab\trending music in data science"

print(f"--- Đang kiểm tra folder: {duong_dan_folder} ---")

# Kiểm tra xem folder này có tồn tại không
if os.path.exists(duong_dan_folder):
    print("Folder có tồn tại! Dưới đây là danh sách file bên trong:\n")
    
    danh_sach_file = os.listdir(duong_dan_folder)
    
    # In ra từng file để bạn so sánh
    tim_thay = False
    for ten_file in danh_sach_file:
        print(f"  {ten_file}")
        if "trending music" in ten_file:
            tim_thay = True
            
    print("\n------------------------------------------------")
    if tim_thay:
        print("GỢI Ý: Hãy copy CHÍNH XÁC tên file bạn thấy ở trên (bao gồm cả .txt) vào code cũ.")
else:
    print("LỖI LỚN: Máy tính báo folder này không tồn tại. Hãy kiểm tra lại đường dẫn từ Desktop trở đi.")