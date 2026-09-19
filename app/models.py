# app/models.py
#
# This file defines the database models for the Automated Resume Parser using SQLAlchemy.
# The 'Candidate' table stores all parsed candidate profiles extracted from resume PDFs.

from datetime import datetime
from app import db


class Candidate(db.Model):
    """
    Candidate Database Model
    Stores candidate profiles parsed by spaCy, PDFPlumber, and Regex.
    """
    __tablename__ = 'candidates'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    skills = db.Column(db.JSON, nullable=True)        # Saved as JSON list
    education = db.Column(db.JSON, nullable=True)     # Saved as JSON list
    experience = db.Column(db.JSON, nullable=True)    # Saved as JSON list
    raw_text = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """
        Helper method to convert a candidate record into a Python dictionary.
        """
        return {
            'id': self.id,
            'filename': self.filename,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'skills': self.skills or [],
            'education': self.education or [],
            'experience': self.experience or [],
            'raw_text': self.raw_text,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

    def __repr__(self):
        return f"<Candidate id={self.id} name='{self.name}' email='{self.email}'>"
