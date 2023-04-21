from flask import Blueprint, render_template, request, jsonify, current_app, redirect, url_for, flash, session
from app.survey import survey_blueprint
from .create_sociogram import create_sociogram
import igraph as ig
import csv
import base64
import os

# login section
test_bp = Blueprint('test_bp', __name__)

def check_credentials(username, password):
    csv_path = os.path.join(os.path.dirname(__file__), 'static', 'data', 'users.csv')
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == username and row['password'] == password:
                return True
    return False

@test_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Username: {username}, Password: {password}")  # Debugging print statement
        if check_credentials(username, password):
            session['logged_in'] = True
            flash('You are now logged in', 'success')
            return redirect(url_for('test_bp.sociogram'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html', user=is_logged_in())

@test_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('test_bp.index'))

def is_logged_in():
    return 'logged_in' in session and session['logged_in']

@test_bp.route('/')
def root():
    return redirect(url_for('test_bp.index'))

# normal pages section

@test_bp.route('/about')
def about():
    return render_template('about.html', user=is_logged_in())

@test_bp.route('/index')
def index():
    return render_template('index.html', user=is_logged_in())

@test_bp.route('/science')
def science():
    return render_template('science.html', user=is_logged_in())

@test_bp.route('/sociogram')
def sociogram():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('test_bp.login'))
    return render_template('sociogram.html', user=is_logged_in())

@test_bp.route('/test')
def test():
    return render_template('test.html', user=is_logged_in())

@test_bp.route('/sociogram-image', methods=['GET'])
def sociogram_image():
    class_name = request.args.get('class')
    if class_name:
        try:
            create_sociogram(class_name)
            with open("sociogram.png", "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            os.remove("sociogram.png")
            return jsonify(encoded_image)
        except Exception as e:
            current_app.logger.error(f'Error while generating sociogram: {str(e)}')
            return "An error occurred while generating the sociogram.", 500
    else:
        return "Please provide a class name to filter the sociogram.", 400

