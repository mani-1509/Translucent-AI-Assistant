from flask import Flask, render_template , Blueprint , url_for , redirect

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('index.html')

@routes.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))

