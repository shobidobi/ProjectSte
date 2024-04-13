from flask import Flask, request, jsonify
from flask_cors import CORS

from API import ForgotPassword,SignUp,Login,Controller_File

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

app.register_blueprint(ForgotPassword.forgot_password_route)
app.register_blueprint(SignUp.signup_route)
app.register_blueprint(Login.login_route)
app.register_blueprint(Controller_File.file_route)


if __name__ == "__main__":
    app.run(debug=True)
