from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

def generate_uuid():
    return str(uuid.uuid4())

# User Model
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# User Preferences Model
class UserPreferences(db.Model):
    __tablename__ = 'user_preferences'
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), primary_key=True)
    voice_style = db.Column(db.String(50), default='formal')
    response_detail_level = db.Column(db.String(50), default='detailed')
    transparency_mode = db.Column(db.Boolean, default=True)
    privacy_mode = db.Column(db.Boolean, default=False)

# Interaction Logs Model
class InteractionLog(db.Model):
    __tablename__ = 'interaction_logs'
    log_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    query = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    reasoning = db.Column(db.JSON, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Custom AI Rules Model
class CustomAIRule(db.Model):
    __tablename__ = 'custom_ai_rules'
    rule_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    rule_description = db.Column(db.Text, nullable=False)
    rule_logic = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# AI Feedback Model
class AIFeedback(db.Model):
    __tablename__ = 'ai_feedback'
    feedback_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    log_id = db.Column(db.String(36), db.ForeignKey('interaction_logs.log_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_correction = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# API Routes
# @app.route('/register', methods=['POST'])
# def register():
#     data = request.json
#     new_user = User(username=data['username'], email=data['email'], password_hash=data['password'])
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({'message': 'User registered successfully!'}), 201

# @app.route('/log_interaction', methods=['POST'])
# def log_interaction():
#     data = request.json
#     new_log = InteractionLog(user_id=data['user_id'], query=data['query'], ai_response=data['ai_response'], reasoning=data['reasoning'])
#     db.session.add(new_log)
#     db.session.commit()
#     return jsonify({'message': 'Interaction logged successfully!'}), 201

# @app.route('/set_preferences', methods=['POST'])
# def set_preferences():
#     data = request.json
#     prefs = UserPreferences.query.filter_by(user_id=data['user_id']).first()
#     if prefs:
#         prefs.voice_style = data.get('voice_style', prefs.voice_style)
#         prefs.response_detail_level = data.get('response_detail_level', prefs.response_detail_level)
#         prefs.transparency_mode = data.get('transparency_mode', prefs.transparency_mode)
#         prefs.privacy_mode = data.get('privacy_mode', prefs.privacy_mode)
#     else:
#         prefs = UserPreferences(**data)
#         db.session.add(prefs)
#     db.session.commit()
#     return jsonify({'message': 'Preferences updated successfully!'}), 200
