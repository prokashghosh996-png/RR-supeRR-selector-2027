import pandas as pd
import hashlib

def get_hash(filepath):
    h = hashlib.md5()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192 * 1024):
            h.update(chunk)
    return h.hexdigest()

f1 = 'd:/Download/RR Auction/Data Pack/ball_by_ball.csv'
f2 = 'd:/Download/RR Auction/new_dataset.csv'

h1 = get_hash(f1)
h2 = get_hash(f2)

print(f"Hash of Data Pack/ball_by_ball.csv: {h1}")
print(f"Hash of new_dataset.csv:           {h2}")
print(f"Exact byte match: {h1 == h2}")

df1 = pd.read_csv(f1)
df2 = pd.read_csv(f2)

print(f"df1 rows: {len(df1)}, cols: {len(df1.columns)}")
print(f"df2 rows: {len(df2)}, cols: {len(df2.columns)}")

matches1 = set(df1['match_id'].unique())
matches2 = set(df2['match_id'].unique())

print(f"Matches in df1: {len(matches1)}")
print(f"Matches in df2: {len(matches2)}")
print(f"Matches in df2 not in df1: {len(matches2 - matches1)}")
print(f"Matches in df1 not in df2: {len(matches1 - matches2)}")

# Check if differences exist anywhere
diff = df1.compare(df2) if df1.shape == df2.shape else "Different shapes"
if isinstance(diff, pd.DataFrame):
    print(f"Differences count: {len(diff)}")
    if len(diff) > 0:
        print(diff.head(10))
else:
    print(diff)
