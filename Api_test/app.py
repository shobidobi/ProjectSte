from flask import Flask
from Api_test.routes import main
from events import socketio

def create_app():
    """
    Create and configure the Flask app.
    :return: The configured Flask app.
    """
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'secret'
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
    app.register_blueprint(main)
    return app


if __name__ == '__main__':
    app = create_app()
    socketio.init_app(app)
    socketio.run(app, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)
