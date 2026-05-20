from recommender import df


song_name = 'Lowdown'
if song_name in df['name'].tolist():
    song_data = df[df['name'] == song_name]
    print(f"Artist-> {song_data['artists'].values.item()}")
    print(f"Mood -> {song_data['mood'].values.item()}")
else:
    print('Not found')
# print(df.columns)