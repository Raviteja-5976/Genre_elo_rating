# GenreRanker: Movie Genre Comparison Tool

## Overview
GenreRanker is a web application that allows users to compare movie genres head-to-head. It uses an Elo-based rating system to determine both personalized and global favorite genres. Users can select a set of genres, compare them in pairs, and see their personalized ranking. The application also aggregates scores from all users to display a "World Favorites" list.

## Features
*   **Genre Selection:** Users can select multiple genres they are interested in comparing.
*   **Pairwise Comparison:** Presents pairs of selected genres for users to vote on their preference.
*   **Elo Rating System:** Dynamically calculates and updates genre scores based on comparison outcomes.
*   **Personalized Rankings:** Displays a ranked list of genres based on the user's session comparisons.
*   **World Favorites:** Shows a global ranking of genres based on aggregated scores from all user interactions.
*   **Database Integration:** Stores genre names and their Elo scores persistently.
*   **Automatic Database Initialization:** Creates the necessary database schema and populates initial genre data if not already present.

## Technology Stack
*   **Backend:** Python, Flask
*   **Database:** SQLAlchemy (with support for SQLite and PostgreSQL)
*   **Frontend:** HTML, CSS, JavaScript (via Flask templates)
*   **Deployment (Production):** Gunicorn

## File Structure
```
.
├── main.py               # Main Flask application, routes, and core logic
├── models/
│   ├── models.py         # SQLAlchemy database models (Genre)
│   └── movie_recommend.py # Placeholder for future movie recommendation features
├── templates/            # HTML templates for web pages
├── instance/
│   └── genres.db         # Default SQLite database file
├── requirements.txt      # Python package dependencies
├── Procfile              # Heroku deployment configuration
├── LICENSE               # Project license
└── README.md             # This file
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

### Development
To run the application in a development environment:
```bash
python main.py
```
The application will be accessible at `http://127.0.0.1:5000/`.

### Production
For production, Gunicorn can be used as specified in the `Procfile`:
```bash
gunicorn main:app
```
Ensure your environment variables (like `DATABASE_URL` and `SECRET_KEY`) are set appropriately for production.

## Database
The application uses SQLite by default, with the database file located at `instance/genres.db`.
It can be configured to use a PostgreSQL database by setting the `DATABASE_URL` environment variable.
The database schema consists of a single `Genre` table with columns for `id`, `name` (unique), and `score` (Elo rating).

The application automatically initializes the database and populates the `Genre` table with a predefined list of genres if they don't already exist, each starting with a score of 0. This score is then updated based on user comparisons.

## Future Development
The `models/movie_recommend.py` file is currently a placeholder. Future development could include integrating movie data and providing recommendations based on ranked genres.

## License
This project is licensed under the terms of the LICENSE file.
