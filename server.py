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
    base_dir = '/mnt/code/output/'
    all_files = []
    
    for root, _, files in os.walk(base_dir):
        for file in files:
            relative_path = os.path.relpath(root, base_dir)
            if relative_path == '.':
                relative_path = ''
            full_path = os.path.join(relative_path, file)
            all_files.append(full_path)
    
    return jsonify(all_files)

@app.route('/file/<filename>')
def serve_specific_file(filename):
    base_dir = '/mnt/code/output/'
    
    # Search for the file in the directory and its subdirectories
    for root, _, files in os.walk(base_dir):
        if filename in files:
            file_path = os.path.join(root, filename)
            return send_file(file_path, as_attachment=True)
    
    return "File not found", 404

if __name__ == '__main__':
    print("Server starting...")
    app.run(host='0.0.0.0', port=5000)