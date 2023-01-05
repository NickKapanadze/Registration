from flask import Flask, jsonify
import os

ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

@app.route('/')
def index():
    return 'Flask is running!'

if __name__ == '__main__':
    
    app.run(ssl_context="reg.app", port=3030)