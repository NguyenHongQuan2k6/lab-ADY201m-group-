from pymongo import MongoClient, UpdateOne
import requests
from datetime import datetime
import re

# ============================================================
# CẤU HÌNH & LẤY DỮ LIỆU TỪ LAST.FM
# ============================================================
LASTFM_API_KEY = "1d3859b87ffb2793f01200613e64bda5"
_tracks = None

for _country in ["Viet Nam", "Vietnam", "VN"]:
    try:
        _res = requests.get(
            "https://ws.audioscrobbler.com/2.0/",
            params={"method": "geo.gettoptracks", "country": _country, "api_key": LASTFM_API_KEY, "format": "json", "limit": 50},
            headers={"User-Agent": "MusicData/1.0"},
            timeout=15
        )
        _data = _res.json()
        if "error" not in _data:
            _tracks = _data["tracks"]["track"]
            break
    except:
        continue

if not _tracks:
    _res = requests.get(
        "https://ws.audioscrobbler.com/2.0/",
        params={"method": "chart.gettoptracks", "api_key": LASTFM_API_KEY, "format": "json", "limit": 50},
        headers={"User-Agent": "MusicData/1.0"},
        timeout=15
    )
    _tracks = _res.json()["tracks"]["track"]

# ============================================================
# XỬ LÝ DỮ LIỆU (Theo Schema mới)
# ============================================================
list_top_trending = []
gio_co_dinh = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
print(f"Bắt đầu quét Last.fm lúc: {gio_co_dinh}")

for index in range(len(_tracks)):
    track = _tracks[index]
    try:
        song_name  = track["name"]
        artist     = track["artist"]["name"] if isinstance(track["artist"], dict) else track["artist"]
        
        cover_image_url = "N/A"
        if "image" in track and isinstance(track["image"], list) and len(track["image"]) > 0:
            cover_image_url = track["image"][-1].get("#text", "N/A")

        song_url   = track.get("url", "N/A")
        listeners  = int(track.get("listeners", 0)) 

        song_dict = {
            "title": song_name,                     
            "artist": artist,                       
            "genre": "N/A",                         
            "cover_image_url": cover_image_url,     
            "platform": "Last.fm",                  
            "trending_date": gio_co_dinh,           
            "song_url": song_url,                   
            "lastfm_listeners": listeners           
        }

        list_top_trending.append(song_dict)
    except Exception as e:
        continue

# ==========================================
# CẬP NHẬT DỮ LIỆU & GỘP BÀI HÁT TRÙNG TÊN
# ==========================================
if list_top_trending: 
    print("\n--- ĐANG CẬP NHẬT LAST.FM VÀO MONGODB ---")
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
            print(" Đã đồng bộ dữ liệu Last.fm theo chuẩn mới!")
            
    except Exception as e:
        print(f" Có lỗi khi cập nhật: {e}")