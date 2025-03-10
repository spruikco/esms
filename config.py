# config.py
import os

class Config:
    """Application configuration settings"""
    SECRET_KEY = 'your_secret_key_here'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # Limit file size to 1MB
    SQLALCHEMY_DATABASE_URI = 'sqlite:///esms.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Match engine configurations
    SUBSTITUTIONS = 3  # Default number of substitutions allowed
    HOME_BONUS = 150   # Home advantage bonus
    
    # Add more configuration settings as needed