from flask import Flask, render_template , Blueprint , url_for , redirect , request , jsonify , session
from werkzeug.security import generate_password_hash, check_password_hash
from src.database import db , User , UserPreferences , InteractionLog , CustomAIRule , AIFeedback

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('index.html')

@routes.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))

# User registration
@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        email = data.get('email')
        password = generate_password_hash(data.get('password'))

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already taken"}), 400

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('routes.login'))
    return render_template('register.html')

# User login
@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({"error": "Invalid username or password"}), 400

        session['user_id'] = user.id
        return redirect(url_for('routes.index'))

    return render_template('login.html')

# User logout
@routes.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('routes.index'))