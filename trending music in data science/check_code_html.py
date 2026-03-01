file_dau_vao = r"C:\Users\hongq\OneDrive\Desktop\Python\ADY201m\lab\trending music in data science\information_web.txt"

try:
    with open(file_dau_vao, "r", encoding="utf-8") as f_in:
        information_page = f_in.read()

    print("Đã đọc xong file! Đang kiểm tra nội dung...\n")
    
    # --- THÊM ĐOẠN NÀY ĐỂ XEM NỘI DUNG ---
    print("=" * 30)
    print("NỘI DUNG THỰC TẾ TRONG FILE LÀ:")
    print(information_page[:1000])  # Chỉ in 1000 ký tự đầu tiên để tránh bị tràn màn hình
    print("=" * 30)
    print(f"Tổng số ký tự trong file: {len(information_page)}")
    # -------------------------------------

    # ... (Giữ nguyên đoạn code tìm kiếm phía sau của bạn) ...

except FileNotFoundError:
    print("Vẫn chưa tìm thấy file!")