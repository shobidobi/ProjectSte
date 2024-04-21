from flask import Flask, request, jsonify
from flask_cors import CORS

from Entity.e import getSession

from app import socketio, app

@app.route('/codecompany', methods=['POST'])
def code_company():

    Session = getSession()
    session = Session()




if __name__ == "__main__":
    app.run(debug=True)
