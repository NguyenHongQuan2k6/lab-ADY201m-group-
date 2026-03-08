import pandas as pd
import database_Lastfm as mp

# 1. Bế thẳng danh sách dữ liệu từ mainpage vào Pandas
df = pd.DataFrame(mp.list_top_trending)

# 2. Sắp xếp lại thứ tự cột cho đẹp
df = df[["Time", "Song Rank", "Song Name", "Artist", "Listeners"]]

# 3. In ra màn hình
print(f"\nFound the top {len(mp.list_top_trending)} trending Vpop songs\n")
print(df.to_markdown(index=False))
