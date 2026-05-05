import pandas as pd
import numpy as np

df = pd.read_csv('spotify_clean.csv')
feature_cols = ['danceability', 'energy','loudness', 'speechiness', 'acousticness', 'instrumentalness','liveness', 'valence', 'tempo']


condition = [
    (df['energy']>1.0),
    (df['valence']>0) & (df['energy']> 0.5) & (df['energy']<=1.0),
    (df['valence']< 0) & (df['energy']< 0),
    (df['energy']<= 0) & (df['valence']>=0)
]

choices = ['workout','happy','sad','focus']

df['mood'] = np.select(condition,choices,default='neutral')

drop_cols = ['id','name','artists','explicit','year','mood']
feature_matrix = df.drop(columns=drop_cols)
def cosine_similarity_scratch(matA,matB):
    # cosine-similarity =  (matA . matB)/ sqrt(((matA.sum)**2).sum() * sqrt(((matB.sum)**2).sum())
    matA,matB = matA.values,matB.values
    dot_product= np.dot(matA,matB.T)
    
    squareA = matA ** 2
    squareB = matB ** 2

    sumA = np.sum(squareA,axis=1)
    sumB = np.sum(squareB,axis=1)

    magA = np.sqrt(sumA)
    magB = np.sqrt(sumB)

    mag_mul = np.outer(magA,magB)
    mag_mul = np.where(mag_mul == 0,1e-10,mag_mul)
    result = (dot_product)/mag_mul

    return result

similarity_matrix = cosine_similarity_scratch(feature_matrix,feature_matrix)

def recommendation_engine(song_name,Mood=None,recs = 10):
    matches = df[df['name'] == song_name]

    if len(matches) == 0:
        return None

    idx = matches.index[0]

    row_sm = similarity_matrix[idx]

    sorted_row_sm = np.argsort(row_sm)[::-1]

    recommended_idx = sorted_row_sm[1:50+1]

    song_title = []
    mood = []
    artists = []
    score = []
    for i in recommended_idx:
        song_title.append(df.iloc[i]['name'])
        mood.append(df.iloc[i]['mood'])
        artists.append(df.iloc[i]['artists'])
        score.append(row_sm[i])
    
    data_list = {
        'recommended_songs': song_title,
        'moods': mood,
        'artists': artists,
        'score': score
    }
    result = pd.DataFrame(data_list)
    if Mood:
        filtered = result[result['moods'] == Mood].iloc[:recs]
        if len(filtered) == 0:
            print(f"Not enough {Mood} songs similar to '{song_name}'.")
            print("Showing best matches regardless of mood...")
            return result.iloc[:recs]
        return filtered
    else:
        return result.iloc[:recs]
    

def inject_diversity(result,recs=10):
    top_8 = result.iloc[:recs-2]
    majority_mood = top_8['moods'].value_counts().index[0]
    # For those songs which are not as same with 
    diverse_songs = df[(df['mood'] != majority_mood) & (~df['name'].isin(result['recommended_songs']))].sample(2)
    diverse_df = pd.DataFrame({
    'recommended_songs': diverse_songs['name'].values,
    'moods': diverse_songs['mood'].values,
    'artists': diverse_songs['artists'].values,
    'score': [0.0, 0.0]
    })
    result = result.iloc[:-2]
    final_recommendations = pd.concat([top_8, diverse_df])
    final_recommendations = final_recommendations.reset_index(drop=True)
    return final_recommendations
    

def recommend_v2(song_name, mood=None, n=10):
    result = recommendation_engine(song_name, Mood=mood, recs=n)
    if result is None:
        return None
    final_result = inject_diversity(result, n)
    # mood_display = mood if mood else "No filter"
    # print(f'Recommendation for "{song_name}" | Mood: {mood_display}')
    # print('=' * 60)
    # for i, row in final_result.iterrows():
    #     score_display = "DIVERSITY PICK" if row['score'] == 0.0 else f"{row['score']:.4f}"
    #     print(f"{i+1}. {row['recommended_songs']} — {row['artists']} | Score: {score_display} | {row['moods']}")
    return final_result


if __name__ == '__main__':
    recommend_v2("Trigga", mood="happy")



