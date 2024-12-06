from flask import Flask, send_file, jsonify
import ctypes
import os

app = Flask(__name__)

# Load the Zig-compiled shared library
lib = ctypes.CDLL('./libperformance_module.so')

# Define the function signatures for interfacing with the shared library's functions
process_data = lib.process_data
process_data.argtypes = [ctypes.POINTER(ctypes.c_char), ctypes.c_size_t]
process_data.restype = ctypes.c_int

list_files = lib.list_files
list_files.argtypes = [ctypes.POINTER(ctypes.c_char)]
list_files.restype = None

serve_file = lib.serve_file
serve_file.argtypes = [ctypes.POINTER(ctypes.c_char)]
serve_file.restype = ctypes.c_void_p

@app.route('/')
def hello():
    # Endpoint returning a greeting message
    return "Hello, World!"

@app.route('/get_parquet/<path:path>')
def get_parquet(path):
    # Endpoint to get a specific parquet file
    file_path = os.path.join('/mnt/', path).encode('utf-8')
    file_content = serve_file(file_path)
    if file_content:
        return send_file(file_content, as_attachment=True)
    return "File not found", 404

@app.route('/list_files')
def list_files_endpoint():
    # Endpoint to list files in a specific directory
    base_dir = '/mnt/code/output/'.encode('utf-8')
    list_files(base_dir)
    # Note: This is a simplified example. In practice, you'd need to pass back results.
    return jsonify({"status": "Files listed"})

@app.route('/file/<filename>')
def serve_specific_file(filename):
    # Endpoint to serve a specific file by filename
    base_dir = '/mnt/code/output/'.encode('utf-8')
    file_path = os.path.join(base_dir.decode(), filename).encode('utf-8')
    file_content = serve_file(file_path)
    if file_content:
        return send_file(file_content, as_attachment=True)
    return "File not found", 404

@app.route('/process_data')
def process_data_endpoint():
    # Endpoint to process data using a shared library function
    data = b"Some data to process"
    result = process_data(data, len(data))
    return jsonify({"result": result})

if __name__ == '__main__':
    # Start the Flask server
    print("Server starting...")
    app.run(host='0.0.0.0', port=5000)