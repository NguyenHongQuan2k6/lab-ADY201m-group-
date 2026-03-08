from pymongo import MongoClient, UpdateOne
import requests
from bs4 import BeautifulSoup
import re 
from datetime import datetime 
import filter_data_in_each_songs as code_in_each_songs

# ============================================================
# CẤU HÌNH & LẤY DỮ LIỆU NHACCUATUI
# ============================================================
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
url_get = 'https://www.nhaccuatui.com/chart/1-5-d64-2026'
r_main_page = requests.get(url_get, headers=headers)

list_top_trending = []

if r_main_page.status_code == 200:
    soup = BeautifulSoup(r_main_page.text, 'html.parser')
    
    music = soup.find_all('div', class_='song-item')
    list_links = code_in_each_songs.danh_sach_ket_qua

    gio_co_dinh = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"Bắt đầu quét Nhaccuatui lúc: {gio_co_dinh}")

    for index in range(len(music)):
        song = music[index] 
        
        try:
            song_name = song.find('div', class_='song-name').text.strip()
            artist = song.find('span', class_="name-text").text.strip()
            
            url_song = list_links[index] if index < len(list_links) else "N/A"
            
            cover_image_url = "N/A"
            img_tag = song.find('img')
            if img_tag and img_tag.has_attr('src'):
                cover_image_url = img_tag['src']

            heart_hien_thi = "0" 
            
            if url_song != "N/A" and url_song.startswith("http"):
                try:
                    r_detail = requests.get(url_song, headers=headers, timeout=5)
                    if r_detail.status_code == 200:
                        tim_heart = re.search(r'(\d+),"http://log4x', r_detail.text)
                        if tim_heart:
                            heart_hien_thi = tim_heart.group(1)
                except: pass

            song_dict = {
                "title": song_name,                     
                "artist": artist,                       
                "genre": "N/A",                         
                "cover_image_url": cover_image_url,     
                "platform": "Nhaccuatui",               
                "trending_date": gio_co_dinh,           
                "song_url": url_song,                   
                "nct_hearts": int(heart_hien_thi) if heart_hien_thi.isdigit() else 0
            }            
            list_top_trending.append(song_dict)

        except AttributeError:
            continue

# ==========================================
# CẬP NHẬT DỮ LIỆU & GỘP BÀI HÁT TRÙNG TÊN
# ==========================================
if list_top_trending: 
    print("\n--- ĐANG CẬP NHẬT VÀ GỘP DỮ LIỆU TRONG MONGODB ---")
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['trending_music_in_Vietnam_db']
        collection = db['bang_xep_hang']
        
        cac_thao_tac = []
        for bai_hat in list_top_trending:
            tieu_de = bai_hat.get("title").strip()
            
            dieu_kien_tim_thong_minh = {"title": {"$regex": f"^{re.escape(tieu_de)}$", "$options": "i"}}
            bai_hat_cu = collection.find_one(dieu_kien_tim_thong_minh)
            
            if bai_hat_cu:
                lenh = UpdateOne({"_id": bai_hat_cu["_id"]}, {"$set": bai_hat})
            else:
                dieu_kien_tao_moi = {"title": tieu_de, "artist": bai_hat.get("artist")}
                lenh = UpdateOne(dieu_kien_tao_moi, {"$set": bai_hat}, upsert=True)
                
            cac_thao_tac.append(lenh)
            
        if cac_thao_tac:
            collection.bulk_write(cac_thao_tac)

        # ==========================================
        # BƯỚC ĐỘT PHÁ: TÍNH ĐIỂM, ĐÁNH RANK & LƯỢT TĂNG TRƯỞNG
        # ==========================================
        print("\n--- ĐANG ĐÁNH RANK VÀ TÍNH TOÁN LƯỢT TĂNG ---")
        tat_ca_bai_hat = list(collection.find({})) 
        
        for bai in tat_ca_bai_hat:
            diem_lastfm = bai.get("lastfm_listeners", 0)
            diem_nct = bai.get("nct_hearts", 0)
            
            # 1. Tính tổng điểm MỚI
            diem_moi = diem_lastfm + diem_nct
            
            # 2. Lấy tổng điểm CŨ (đã lưu trong DB từ lần chạy trước)
            diem_cu = bai.get("views_or_streams", 0)
            
            # 3. Tính lượt tăng trưởng
            luot_tang = diem_moi - diem_cu
            
            # Gán vào biến tạm
            bai["views_or_streams"] = diem_moi
            bai["daily_increase"] = luot_tang
            
            # Xử lý gộp tên Platform
            if diem_lastfm > 0 and diem_nct > 0:
                bai["platform"] = "Last.fm & Nhaccuatui"
            elif diem_lastfm > 0:
                bai["platform"] = "Last.fm"
            else:
                bai["platform"] = "Nhaccuatui"

        # Sắp xếp danh sách dựa trên views_or_streams
        tat_ca_bai_hat.sort(key=lambda x: x["views_or_streams"], reverse=True)

        # Lưu thứ hạng và dữ liệu mới ngược lại vào Database
        thao_tac_xep_hang = []
        for thu_tu, bai in enumerate(tat_ca_bai_hat):
            hang_moi = str(thu_tu + 1) 
            
            dieu_kien = {"_id": bai["_id"]}
            cap_nhat = {"$set": {
                "rank": hang_moi, 
                "views_or_streams": bai["views_or_streams"],
                "daily_increase": bai["daily_increase"], # Lưu cột tăng trưởng vào DB
                "platform": bai["platform"]
            }}
            thao_tac_xep_hang.append(UpdateOne(dieu_kien, cap_nhat))

        if thao_tac_xep_hang:
            collection.bulk_write(thao_tac_xep_hang)
            print(" Hoàn tất! Database đã cập nhật Schema mới và có cột Tăng trưởng.")
            
    except Exception as e:
        print(f" Có lỗi khi cập nhật: {e}")