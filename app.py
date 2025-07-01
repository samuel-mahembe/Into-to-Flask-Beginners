from flask import Flask, request, jsonify
import face_recognition
import os
from flask_cors import CORS


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
CORS(app)
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return jsonify({'file': file.filename})


@app.route('/compare-faces', methods=['POST'])
def compare_faces():
    if 'selfie' not in request.files or 'idface' not in request.files:
        return jsonify({'error': 'Missing files'}), 400

    selfie = request.files['selfie']
    idface = request.files['idface']

    selfie_path = os.path.join(UPLOAD_FOLDER, 'selfie.jpg')
    idface_path = os.path.join(UPLOAD_FOLDER, 'idface.jpg')

    selfie.save(selfie_path)
    idface.save(idface_path)

    try:
        selfie_img = face_recognition.load_image_file(selfie_path)
        id_img = face_recognition.load_image_file(idface_path)

        selfie_encoding = face_recognition.face_encodings(selfie_img)[0]
        id_encoding = face_recognition.face_encodings(id_img)[0]

        results = face_recognition.compare_faces([id_encoding], selfie_encoding)
        distance = face_recognition.face_distance([id_encoding], selfie_encoding)[0]

        return jsonify({
            'match': str(results[0]),
            'confidence': float(1 - distance)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run()
