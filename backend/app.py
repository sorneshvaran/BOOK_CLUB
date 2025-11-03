from flask import Flask, send_from_directory
from flask_cors import CORS
from api import api_bp
import os

frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
app = Flask(__name__, static_folder=frontend_path, static_url_path='')
CORS(app)

app.register_blueprint(api_bp)

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)