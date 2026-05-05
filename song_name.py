import pandas as pd
df = pd.read_csv('spotify_clean.csv')
print(df[df['name'] == 'Falling'])