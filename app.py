from flask import Flask, request, jsonify
# import face_recognition
import os
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return jsonify({'file': file.filename})

if __name__ == '__main__':
    app.run()
