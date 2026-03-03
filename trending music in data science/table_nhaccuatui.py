import pandas as pd
import mainpage_nhaccuatui as mp

# Bế thẳng danh sách dữ liệu từ mainpage vào Pandas
df = pd.DataFrame(mp.list_top_trending)

# Xử lý dữ liệu trùng
df = df.drop_duplicates(subset=["Song name", "Artist"])

# Sắp xếp lại thứ tự cột cho đẹp (bỏ qua bước read_csv)
df = df[["Time", "Date Updated", "Song name", "Song rank", "Artist", "Hearts (Real)", "Shares (Real)"]]

# In ra màn hình => Kiểm tra tổng quan dữ liệu
print(f"\nFound the top {len(mp.list_top_trending)} trending Vpop songs\n")
print(df.to_markdown(index=False))
