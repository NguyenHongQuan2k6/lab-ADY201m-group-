import pandas as pd
import mainpage_nhaccuatui as mp

# 1. Bế thẳng danh sách dữ liệu từ mainpage vào Pandas
df = pd.DataFrame(mp.list_top_trending)

# 2. Sắp xếp lại thứ tự cột cho đẹp (bỏ qua bước read_csv)
df = df[["Time", "Date Updated", "Song name", "Song rank", "Artist", "Hearts (Real)", "Shares (Real)"]]

# 3. In ra màn hình
print(f"\nFound the top {len(mp.list_top_trending)} trending Vpop songs\n")
print(df.to_markdown(index=False))