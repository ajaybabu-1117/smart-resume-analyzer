from . import db
from datetime import datetime

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    raw_text = db.Column(db.Text, nullable=False)
    match_percent = db.Column(db.Float, nullable=False)
    skills = db.Column(db.Text, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
