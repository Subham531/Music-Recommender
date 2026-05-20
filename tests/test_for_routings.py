import pytest
from main import app as flask_app
import sys
import os
import pandas as pd


sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
))


mock_df = pd.DataFrame({
    'name':    ['And You Are There', 'Lowdown', 'The Last Island'],
    'artists': ['Damon & Naomi', 'Delta Moon', 'Peter Mayer'],
    'mood':    ['happy', 'sad', 'focus'],
})

mock_recommendations = pd.DataFrame({
    'recommended_songs': ['Lowdown', 'The Last Island'],
    'artists':           ['Delta Moon', 'Peter Mayer'],
    'moods':             ['neutral', 'neutral'],
})

fake_recommender = type(sys)('recommender')
fake_recommender.recommend_v2 = lambda song, mood=None: mock_recommendations
fake_recommender.df = mock_df
sys.modules['recommender'] = fake_recommender


@pytest.fixture
def test_client():
    flask_app.config['TESTING'] = True
    flask_app.config['SECRET_KEY'] = 'test-secret'  
    with flask_app.test_client() as c:
        yield c


@pytest.fixture
def logged_in_client(test_client):  
    with test_client.session_transaction() as sess:
        sess['user_id'] = 'fake_user_id_123'
        sess['name'] = 'Test User'
    return test_client


# ===== TESTS =====

def test_home_redirects_when_not_logged_in(test_client):  
    res = test_client.get('/')
    assert res.status_code == 302
    assert '/login' in res.headers['Location']


def test_login_get(test_client):  
    res = test_client.get('/login')
    assert res.status_code == 200


def test_signup_get(test_client):  
    res = test_client.get('/signup')
    assert res.status_code == 200


def test_search_short_query_returns_empty(test_client):  
    res = test_client.get('/search?q=S')
    assert res.get_json() == {'results': []}


def test_search_returns_results(test_client):  
    res = test_client.get('/search?q=And')
    data = res.get_json()
    assert 'results' in data
    assert len(data['results']) > 0


def test_recommend_redirects_when_not_logged_in(test_client):  
    res = test_client.post('/recommend', data={'song_name': 'Song A', 'mood': ''})
    assert res.status_code == 302
    assert '/login' in res.headers['Location']


def test_history_redirects_when_not_logged_in(test_client):  
    res = test_client.get('/history')
    assert res.status_code == 302
    assert '/login' in res.headers['Location']


def test_home_accessible_when_logged_in(logged_in_client):
    res = logged_in_client.get('/')
    assert res.status_code == 200


def test_logout_clears_session(logged_in_client):
    res = logged_in_client.get('/logout')
    assert res.status_code == 302
    with logged_in_client.session_transaction() as sess:
        assert 'user_id' not in sess