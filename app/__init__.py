from flask import Flask
from .routes import test_bp

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.register_blueprint(test_bp)

    return app
