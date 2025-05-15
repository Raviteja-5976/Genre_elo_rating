from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    score = db.Column(db.Float, default=1500)  # Default Elo rating

    def __repr__(self):
        return f'<Genre {self.name}>'