from flask import Flask
from Api_test.routes import main
from events import socketio

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'secret'
    app.register_blueprint(main)
    return app

if __name__ == '__main__':
    app = create_app()
    socketio.init_app(app)
    socketio.run(app, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)
