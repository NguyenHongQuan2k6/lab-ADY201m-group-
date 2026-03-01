import get_information_web
file_dau_vao = "information_web.txt"

# --- Phần còn lại giữ nguyên ---
file_ket_qua = "link_song.txt"

try:
    
    with open(file_dau_vao, "r", encoding="utf-8") as f_in:
        information_page = f_in.read()

    start_marker = "https://www.nhaccuatui.com/song/"
    len_marker = len(start_marker) # Độ dài đoạn https... (khoảng 32 ký tự)
    ky_tu_muon_lay_them = 12       # Số ký tự mã bài hát phía sau
    
    danh_sach_ket_qua = [] # Tạo một cái rổ để chứa các link tìm được
    vi_tri_bat_dau_tim = 0 # Bắt đầu tìm từ con số 0

    # --- BẮT ĐẦU VÒNG LẶP ---
    while True:
        # Tìm vị trí xuất hiện của https..., nhưng tìm từ 'vi_tri_bat_dau_tim'
        search = information_page.find(start_marker, vi_tri_bat_dau_tim)

        # Nếu search == -1 nghĩa là tìm hết file rồi không thấy nữa -> Thoát
        if search == -1:
            break
        
        # Tính toán điểm cắt:
        # Vị trí cắt = Vị trí tìm thấy + Độ dài https + 12 ký tự mã bài
        vi_tri_ket_thuc = search + len_marker + ky_tu_muon_lay_them
        
        # Cắt chuỗi
        link_tim_thay = information_page[search : vi_tri_ket_thuc]
        
        # Thêm vào danh sách
        danh_sach_ket_qua.append(link_tim_thay)
        
        # QUAN TRỌNG NHẤT: Cập nhật vị trí để lần sau tìm tiếp ở phía sau
        vi_tri_bat_dau_tim = vi_tri_ket_thuc

    # --- KẾT THÚC VÒNG LẶP, GIỜ THÌ GHI FILE ---
    

    if len(danh_sach_ket_qua) > 0:
        with open(file_ket_qua, "w", encoding="utf-8") as f_out:
            for link in danh_sach_ket_qua:
                f_out.write(link + "\n") # Ghi từng link và xuống dòng
                #print(link) # In ra màn hình để bạn xem luôn
                
    else:
        print("Không tìm thấy bài nào cả.")

except FileNotFoundError:
    print("\nVAN CHUA DUOC: Python vẫn không tìm thấy file.")
    print("Gợi ý cuối cùng: Có thể file của bạn bị dính lỗi '.txt.txt'.")
    print("Hãy thử sửa dòng file_dau_vao thêm một đuôi .txt nữa xem sao (thành .txt.txt)")