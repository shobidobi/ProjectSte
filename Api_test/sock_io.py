#sock_io.py
from flask_socketio import SocketIO
socketio = SocketIO(cors_allowed_origins="*",max_http_buffer_size=50 * 1024 * 1024)

