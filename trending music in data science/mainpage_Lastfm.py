import requests
from datetime import datetime

# ============================================================
# CẤU HÌNH
# ============================================================
LASTFM_API_KEY = "1d3859b87ffb2793f01200613e64bda5"

# ============================================================
# LẤY DỮ LIỆU TỪ LAST.FM
# ============================================================
_tracks = None

for _country in ["Viet Nam", "Vietnam", "VN"]:
    try:
        _res = requests.get(
            "https://ws.audioscrobbler.com/2.0/",
            params={
                "method"  : "geo.gettoptracks",
                "country" : _country,
                "api_key" : LASTFM_API_KEY,
                "format"  : "json",
                "limit"   : 50
            },
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
        params={
            "method"  : "chart.gettoptracks",
            "api_key" : LASTFM_API_KEY,
            "format"  : "json",
            "limit"   : 50
        },
        headers={"User-Agent": "MusicData/1.0"},
        timeout=15
    )
    _tracks = _res.json()["tracks"]["track"]

# ============================================================
# XỬ LÝ DỮ LIỆU - giống cấu trúc mainpage_nhaccuatui
# ============================================================
list_top_trending = []

# Lấy thời gian cố định 1 lần duy nhất
gio_co_dinh = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
print(f"Bắt đầu quét lúc: {gio_co_dinh}")

# Dùng range(len(...)) thay vì enumerate - giống code mẫu
for index in range(len(_tracks)):

    track = _tracks[index]

    try:
        song_name  = track["name"]
        song_rank  = str(index + 1)
        artist     = track["artist"]["name"] if isinstance(track["artist"], dict) else track["artist"]
        listeners  = int(track.get("listeners", 0))
        total_plays= int(track.get("playcount", 0))
        url_song   = track.get("url", "N/A")

        song_dict = {
            "Time"        : gio_co_dinh,
            "Song Rank"   : song_rank,
            "Song Name"   : song_name,
            "Artist"      : artist,
            "Listeners"   : listeners,
        }

        list_top_trending.append(song_dict)
        print(f"[{index+1}] {song_name} | Artist: {artist} | Listeners: {listeners:,}")

    except Exception as e:
        print(f"Lỗi bài #{index+1}: {e}")
        continue

print(f"\nHoàn tất! Đã lấy {len(list_top_trending)} bài hát.")