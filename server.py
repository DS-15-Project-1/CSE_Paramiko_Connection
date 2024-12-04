from flask import Flask, send_file, jsonify
import os

app = Flask(__name__)

# Define a route for the root URL
@app.route('/')
def hello():
    # Return a simple greeting message
    return "Hello, World!"

# Define a route to get a parquet file given a relative path
@app.route('/get_parquet/<path:path>')
def get_parquet(path):
    # Construct the full file path using the base directory
    file_path = os.path.join('/mnt/', path)
    # Send the file as an attachment for download
    return send_file(file_path, as_attachment=True)

# Define a route to list all files in a directory
@app.route('/list_files')
def list_files():
    # Base directory to start the file search
    base_dir = '/mnt/code/output/'
    # Initialize an empty list to store file paths
    all_files = []

    # Traverse the directory structure
    for root, _, files in os.walk(base_dir):
        for file in files:
            # Get the relative path of the directory
            relative_path = os.path.relpath(root, base_dir)
            # If the relative path is the current directory, set it to an empty string
            if relative_path == '.':
                relative_path = ''
            # Construct the full path for each file
            full_path = os.path.join(relative_path, file)
            # Append the full path to the list of all files
            all_files.append(full_path)

    # Return all file paths as a JSON response
    return jsonify(all_files)

# Define a route to serve a specific file by its filename
@app.route('/file/<filename>')
def serve_specific_file(filename):
    # Base directory to start the file search
    base_dir = '/mnt/code/output/'

    # Search for the file in the directory and its subdirectories
    for root, _, files in os.walk(base_dir):
        if filename in files:
            # Construct the full file path and serve the file as an attachment
            file_path = os.path.join(root, filename)
            return send_file(file_path, as_attachment=True)

    # Return a 404 error if the file is not found
    return "File not found", 404

# Start the Flask application
if __name__ == '__main__':
    print("Server starting...")
    # Run the app on all interfaces at port 5000
    app.run(host='0.0.0.0', port=5000)