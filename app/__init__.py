from flask import Flask
from app.routes import init_sistema

def create_app():

    app = Flask(__name__)

    from app.routes import main
    app.register_blueprint(main)

    init_sistema()

    return app