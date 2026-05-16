from sklearn.preprocessing import StandardScaler
import pandas as pd

df = pd.read_csv('Raw_1.2_million.csv')
# print(df.head())


drop_cols = ['album','album_id','artist_ids','track_number','disc_number','key','mode','duration_ms','time_signature','release_date']
df.drop(columns=drop_cols,inplace=True)


df.dropna(inplace=True)
# print(df.isna().sum()) # no null values



df.drop_duplicates(subset=['name','artists'],keep='first',inplace=True,ignore_index=True)

# Dropped from 1204025 to 1141556

# Filtered by year
df = df[df['year'] >= 1990]
df.drop_duplicates(ignore_index=True,inplace=True)


feature_cols = ['explicit','danceability','energy','loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo']

scaler = StandardScaler()
df[feature_cols] = scaler.fit_transform(df[feature_cols])
df[feature_cols]

df = df.sample(n = 20000,random_state = 42,ignore_index = True)
df.to_csv('spotify_clean.csv',index=False)