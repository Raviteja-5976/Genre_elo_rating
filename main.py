import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import pandas as pd
import numpy as np
from itertools import combinations
import random
import json
from models.models import db, Genre

# Define constants
GENRES_LIST = [
    "Action", "Adventure", "Alternate History", "Apocalyptic", "Biography",
    "Body Horror", "Comedy", "Comedy Horror", "Conspiracy Fiction", "Crime Fiction",
    "Dark Comedy", "Detective Fiction", "Drama", "Experimental", "Fairy Tale",
    "Fantasy", "Fiction", "High Fantasy", "Historical Drama", "Historical Fiction",
    "History", "Horror", "Humor", "Magical Realism", "Melodrama",
    "Mystery", "Narrative", "Psychological Horror", "Quotation", "Religious",
    "Review", "Romance", "Romantic Comedy", "Satire", "Science Fiction",
    "Slapstick", "Suspense", "Thriller", "Western"
]

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')  # Required for session management
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///genres.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Initialize database and create genres if they don't exist
def init_db():
    with app.app_context():
        db.create_all()
        # Add all genres if they don't exist
        for genre_name in GENRES_LIST:
            if not Genre.query.filter_by(name=genre_name).first():
                genre = Genre(name=genre_name, score=0)  # Initialize with 0
                db.session.add(genre)
        db.session.commit()

# Initialize the database when the app starts
init_db()

def calculate_expected_score(rating_a, rating_b):
    """Calculates the expected score of player A against player B."""
    return 1 / (1 + 10**((rating_b - rating_a) / 400))

def update_elo(rating_a, rating_b, score_a, k=32):
    """Updates the Elo ratings of two players after a match."""
    expected_a = calculate_expected_score(rating_a, rating_b)
    expected_b = 1 - expected_a
    new_rating_a = rating_a + k * (score_a - expected_a)
    new_rating_b = rating_b + k * ((1 - score_a) - expected_b)
    return new_rating_a, new_rating_b

def get_or_create_genre(name):
    genre = Genre.query.filter_by(name=name).first()
    if not genre:
        genre = Genre(name=name, score=0)  # Initialize with 0
        db.session.add(genre)
        db.session.commit()
    return genre

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/select-genres')
def select_genres():
    shuffled_genres = list(GENRES_LIST)
    random.shuffle(shuffled_genres)
    return render_template('select_genres.html', genres=shuffled_genres)

@app.route('/start-comparison', methods=['POST'])
def start_comparison():
    selected_genres = request.form.getlist('genres')
    if len(selected_genres) < 2:
        return redirect(url_for('select_genres'))
    
    # Initialize ratings and create comparison pairs
    session['selected_genres'] = selected_genres
    session['genre_ratings'] = {}
      # Initialize session ratings with 1500 for fair comparison
    for genre_name in selected_genres:
        genre = get_or_create_genre(genre_name)
        session['genre_ratings'][genre_name] = 1500  # Use 1500 for comparison calculations
        
    session['comparison_pairs'] = list(combinations(selected_genres, 2))
    random.shuffle(session['comparison_pairs'])
    session['comparison_index'] = 0
    session['comparisons_done'] = 0
    
    return redirect(url_for('compare'))

@app.route('/compare')
def compare():
    if 'genre_ratings' not in session:
        return redirect(url_for('select_genres'))
    
    if session['comparison_index'] >= len(session['comparison_pairs']):
        return redirect(url_for('results'))
    
    current_pair = session['comparison_pairs'][session['comparison_index']]
    return render_template('compare.html', 
                         genre1=current_pair[0], 
                         genre2=current_pair[1],
                         total_comparisons=len(session['comparison_pairs']),
                         current_comparison=session['comparison_index'] + 1)

@app.route('/vote', methods=['POST'])
def vote():
    winner = request.json.get('winner')
    loser = request.json.get('loser')
      # Update only session scores during matchups
    rating1 = session['genre_ratings'][winner]
    rating2 = session['genre_ratings'][loser]
    new_rating1, new_rating2 = update_elo(rating1, rating2, 1)
    
    session['genre_ratings'][winner] = new_rating1
    session['genre_ratings'][loser] = new_rating2
    
    session['comparison_index'] += 1
    session['comparisons_done'] += 1
    
    if session['comparison_index'] >= len(session['comparison_pairs']):
        return jsonify({'redirect': url_for('results')})
    return jsonify({'redirect': url_for('compare')})

@app.route('/results')
def results():
    if 'genre_ratings' not in session:
        return redirect(url_for('select_genres'))
    
    # Add the final Elo scores directly to the database
    with app.app_context():
        for genre_name, final_score in session['genre_ratings'].items():
            genre = Genre.query.filter_by(name=genre_name).first()
            if genre:
                # Simply add the final Elo score to the existing score
                genre.score = genre.score + final_score
                db.session.commit()
    
    rankings = sorted(session['genre_ratings'].items(), 
                     key=lambda x: x[1], reverse=True)
    return render_template('results.html', rankings=rankings)

@app.route('/world-favorites')
def world_favorites():
    # Get all genres from database
    genres = Genre.query.all()
    
    # Create a dictionary to store all genres and their scores
    genre_scores = {genre.name: genre.score for genre in genres}
    
    # Make sure all genres from GENRES_LIST are included
    for genre_name in GENRES_LIST:
        if genre_name not in genre_scores:
            # Add missing genres with score 0
            genre_scores[genre_name] = 0
    
    # Create rankings with normalized scores (divided by 1500)
    rankings = [(name, score / 1500) for name, score in genre_scores.items()]
    
    # Sort rankings by score
    rankings.sort(key=lambda x: x[1], reverse=True)
    return render_template('world_favorites.html', rankings=rankings)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)