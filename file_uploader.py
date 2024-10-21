from flask import Flask, request, send_file
import os

from socks import method

app = Flask(__name__)

def upload_file(file_path, destination_folder):
    """
    Uploads a file to a specified destination folder.

    Args:
        file_path: The path to the file to be uploaded.
        destination_folder: The path to the destination folder.
    """

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    try:
        with open(file_path, 'rb') as f:
            with open(os.path.join(destination_folder, os.path.basename(file_path)), 'wb') as dest:
                dest.write(f.read())
        print(f"File uploaded successfully: {file_path}")
        return "File uploaded successfully"
    except Exception as e:
        print(f"Error uploading file: {e}")
        return "Error uploading file"

@app.route('/upload', methods=['POST'])
def upload_file_endpoint():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file:
        destination_folder = 'uploads'

        # Check if the uploads directory exists
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)  # Create it if it doesn't exist

        file_path = os.path.join(destination_folder, file.filename)
        file.save(file_path)
        return upload_file(file_path, destination_folder)

@app.route('/', methods=['GET'])
def home():
    return "Health ok"

if __name__ == '__main__':
    app.run(debug=True)