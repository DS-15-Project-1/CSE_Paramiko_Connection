from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route('/get_parquet/<path:path>')
def get_parquet(path):
    file_path = os.path.join('/mnt/data', path)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
