from flask import Flask
from .routes import test_bp
from .routes import survey_blueprint

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.register_blueprint(test_bp)
    app.register_blueprint(survey_blueprint)

    return app
