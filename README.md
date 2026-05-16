# 🎵 Music Recommender

A Flask-based web application that recommends songs based on similarity to a user's chosen track. The system uses cosine similarity to match songs by audio features and allows users to filter recommendations by mood.

---

## 🌟 Features

- **User Authentication**: Sign up and log in with secure password hashing
- **Song Search**: Search for songs from the Spotify dataset (1.2M+ tracks)
- **Smart Recommendations**: Get song recommendations based on audio features (energy, danceability, valence, etc.)
- **Mood Filtering**: Filter recommendations by mood (workout, happy, sad, focus, neutral)
- **Diversity Injection**: Recommendations include diverse songs to expand musical horizons
- **Search History**: Track your recommendation queries with timestamps
- **Direct Spotify Links**: One-click access to songs on Spotify

---

## 🛠️ Tech Stack

- **Backend**: Flask 3.1.3
- **Database**: MongoDB (user data & search history)
- **Data Processing**: Pandas 3.0.1, NumPy 2.4.3
- **Authentication**: Werkzeug (password hashing)
- **Frontend**: HTML5, CSS3, Jinja2 templating

---

## 📋 Requirements

- Python 3.9+
- MongoDB (local or cloud instance)
- Virtual environment (optional but recommended)

### Dependencies

See `requirement.txt` for all packages. Key dependencies:
```
Flask==3.1.3
pandas==3.0.1
numpy==2.4.3
pymongo==4.16.0
python-dotenv==1.2.2
Werkzeug==3.1.8
scikit-learn==1.8.0
```

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Subham531/Music-Recommender.git
cd Music-Recommender
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirement.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:
```env
Key=your_secret_key_here
MONGO_URL=your_mongodb_connection_string
```

**Example for local MongoDB:**
```env
Key=dev-secret-key-123
MONGO_URL=mongodb://localhost:27017/music_recommender
```

### 5. Prepare Data

Ensure `spotify_clean.csv` is in the project root. This file contains the music dataset with audio features.

### 6. Run the Application
```bash
python app.py
```

The app will start at `http://localhost:5001`

---

## 📁 Project Structure

```
Music_recommender/
├── app.py                      # Main Flask application
├── recommender.py              # Recommendation engine & similarity logic
├── requirement.txt             # Python dependencies
├── spotify_clean.csv           # Music dataset (1.2M+ songs)
├── .env                        # Environment variables (not in git)
│
├── templates/                  # HTML templates
│   ├── index.html             # Home page (song search & recommendation)
│   ├── login.html             # Login form
│   ├── signup.html            # Sign-up form
│   ├── result.html            # Recommendation results page
│   └── history.html           # User search history
│
├── static/                     # Static assets
│   └── styles.css             # CSS styling
│
├── Preprocess/                 # Data preprocessing scripts
│   └── Raw_1.2_million.csv    # Raw Spotify data
│
└── venv/                       # Virtual environment (gitignored)
```

---

## 🎯 How It Works

### 1. **Feature-Based Matching**
The recommendation engine extracts 9 audio features from each song:
- Danceability
- Energy
- Loudness
- Speechiness
- Acousticness
- Instrumentalness
- Liveness
- Valence
- Tempo

### 2. **Cosine Similarity**
Calculates similarity between the query song and all songs in the dataset using cosine similarity:
```
similarity = (A · B) / (||A|| × ||B||)
```

### 3. **Mood Classification**
Songs are classified into moods based on energy and valence:
- **Workout**: High energy songs
- **Happy**: Positive valence + good energy
- **Sad**: Low valence + low energy
- **Focus**: Low valence + moderate energy
- **Neutral**: Default category

### 4. **Diversity Injection**
The top 8 recommendations are combined with 2 songs of different moods to ensure variety.

---

## 📖 Usage Guide

### Sign Up
1. Click "Create an account" on the login page
2. Enter name, email, and password
3. Password is securely hashed before storage

### Login
1. Enter registered email and password
2. Session is created and stored in the database

### Get Recommendations
1. On the home page, search for a song
2. Select it from the dropdown
3. Optionally choose a mood filter
4. Click "Recommend" to see suggestions
5. Each result includes a direct Spotify link

### View History
1. Click "Search History" (available when logged in)
2. View all your past queries with timestamps
3. Mood filters used are also displayed

---

## 🔐 Security Features

- **Password Hashing**: Uses Werkzeug's `generate_password_hash()` for secure password storage
- **Session Management**: User sessions managed via Flask cookies
- **Prepared Queries**: MongoDB queries to prevent injection attacks
- **CSRF Protection**: Can be enabled with Flask-WTF for production

---

## 🐛 Known Issues & Future Improvements

### Current Limitations
- No explicit filtering of already recommended songs
- Mood categories are hardcoded based on energy/valence thresholds
- Dataset limited to pre-processed Spotify data

### Planned Features
- [ ] Advanced filters (decade, artist, genre)
- [ ] User playlists and favorites
- [ ] Real-time Spotify API integration
- [ ] Collaborative filtering recommendations
- [ ] User preference learning
- [ ] Dark mode UI
- [ ] Mobile app (React Native)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👤 Author

**Subham Das**  
GitHub: [@Subham531](https://github.com/Subham531)

---

## 🙋 Support

For issues, questions, or suggestions, please open an [GitHub Issue](https://github.com/Subham531/Music-Recommender/issues).

---

## 🎵 Acknowledgments

- Dataset: Spotify 1.2M tracks
- Built with Flask, MongoDB, and Pandas
- Inspired by content-based filtering recommendation systems

---

**Enjoy discovering new music! 🎧**
