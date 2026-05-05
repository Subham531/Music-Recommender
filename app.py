from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import urllib.parse
from recommender import recommend_v2, df
import os


load_dotenv()

app = Flask(__name__)
app.secret_key = 'music_recommender@123'

# Mongo_url = os.getenv('MONGO_URL')
client = MongoClient('mongodb://localhost:27017/')
db = client['music_recommender']
users_collection = db['users']
history = db['history']


@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_email = users_collection.find_one({'email': email})

        account_exist = request.form
        if existing_email:
            flash('Email already exists', 'warning')
            return redirect(url_for('signup'))

        hashed_psswrd = generate_password_hash(password)

        new_user = {
            'name': name,
            'email': email,
            'password': hashed_psswrd
        }
        # print(new_user)
        users_collection.insert_one(new_user)

        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        existing_email = users_collection.find_one({'email': email})

        if existing_email:

            if check_password_hash(existing_email['password'], password):
                session['user_id'] = str(existing_email['_id'])
                session['name'] = existing_email['name']
                return redirect(url_for('home'))
            else:
                flash('Wrong Password, dude!!', 'warning')
                return redirect(url_for('login'))

        else:
            flash('Email not registered', 'warning')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/search')
def search():
    query = request.args.get('q', '')
    if len(query) < 2:
        return {'results': []}

    matches = df[df['name'].str.contains(
        query, case=False, na=False)]['name'].head(8).tolist()
    return {'results': matches}


@app.route('/recommend', methods=['POST'])
def recommend():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    song_name = request.form.get('song_name')
    mood = request.form.get('mood') or None

    search_entry = {
        'user_id': session['user_id'],
        'song_query': song_name,
        'mood_selected': mood,
        'time_stamp': datetime.now()
    }

    try:
        history.insert_one(search_entry)

    except Exception as e:
        flash(f'Error in saving history: {e}')

    recommendations = recommend_v2(song_name, mood)
    if recommendations is None:
        flash(
            f"Song '{song_name}' not found in our dataset. Please try another song.")
        return redirect(url_for('home'))

    songs = recommendations.to_dict(orient='records')

    for song in songs:
        query = urllib.parse.quote(
            f"{song['recommended_songs']} {song['artists']}"
        )

        song['spotify_url'] = f"https://open.spotify.com/search/{query}"

    return render_template('result.html', songs=songs, mood=mood, query=song_name)


@app.route('/history')
def search_history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_history = list(history.find({'user_id': session['user_id']}).sort('time_stamp',-1))

    return render_template('history.html',history=user_history)



@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
