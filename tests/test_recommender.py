import pytest,sys,os
import pandas as pd
import numpy as np


sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
))

from recommender import feature_cols,recommendation_engine,inject_diversity,recommend_v2,df,feature_matrix,similarity_matrix

 # -------------- Similarity matrix ----------------------
def test_similarity_matrix():
    assert similarity_matrix.shape == (len(df),len(df))

def test_similarity_matrix_diagonal():
    assert abs(similarity_matrix[0][0] - 1.0) < 1e-6
    assert abs(similarity_matrix[3][3] - 1.0) < 1e-6

def test_similarity_matrix_symetric():
    assert np.allclose(similarity_matrix,similarity_matrix.T,atol=1e-6) # symmetric matrix, [Aij = Aji]

# -------------- feature matrix ---------------------
def test_feature_matrix_features():
    assert feature_matrix.columns.tolist() == feature_cols

def test_feature_matrix_no_nulls():
    assert feature_matrix.isnull().sum().sum() == 0



# ------------- inject diversity -----------------------

@pytest.fixture
def sample_recommendation():
    valid_song = df['name'].iloc[0]
    return recommendation_engine(valid_song,recs=10)

def test_inject_diversity_returns_dataframe(sample_recommendation):
    result = inject_diversity(sample_recommendation,recs=10)
    assert isinstance(result,pd.DataFrame)
    

# ------------------ recommend v2 ------------------
def test_recommendation_v2_invalid():
    result = recommendation_engine('asdfghj')
    assert result is None

def test_recommend_v2():
    valid_song = df['name'].iloc[0]
    result = recommend_v2(valid_song)
    assert isinstance(result,pd.DataFrame)
    assert len(result) == 10

def test_recommend_v2_with_mood():
    """Test that recommend_v2 works with mood filter"""
    valid_song = df['name'].iloc[0]
    result = recommend_v2(valid_song, mood='happy')
    assert isinstance(result, pd.DataFrame)
    assert len(result) <= 10  


def test_recommend_v2_columns():
    """Test that recommend_v2 result has required columns"""
    valid_song = df['name'].iloc[0]
    result = recommend_v2(valid_song)
    assert 'name' in result.columns or 'recommended_songs' in result.columns
    assert 'artists' in result.columns


