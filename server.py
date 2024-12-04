from flask import Flask, send_file, jsonify
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/get_parquet/<path:path>')
def get_parquet(path):
    file_path = os.path.join('/mnt/', path)
    return send_file(file_path, as_attachment=True)

@app.route('/list_files')
def list_files():
    files = os.listdir('/mnt/code/output/*')
    return jsonify(files)

if __name__ == '__main__':
    print("Server starting...")
    app.run(host='0.0.0.0', port=5000)