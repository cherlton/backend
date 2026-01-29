from app.extensions import db
from datetime import datetime

class SkillPath(db.Model):
    __tablename__ = "skill_paths"

    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(255), nullable=False)
    steps = db.Column(db.Text, nullable=False)  # stored as JSON string
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
