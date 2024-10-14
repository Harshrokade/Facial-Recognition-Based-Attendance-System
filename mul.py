import os
from flask import Flask, request, jsonify, render_template
import face_recognition
import cv2
import numpy as np
from datetime import datetime

app = Flask(__name__)

# Constants
UPLOAD_FOLDER = 'static/uploads'
DATABASE_FOLDER = 'static/imageData'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_known_faces():
    known_face_encodings = []
    known_face_names = []
    for filename in os.listdir(DATABASE_FOLDER):
        if allowed_file(filename):
            image_path = os.path.join(DATABASE_FOLDER, filename)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                encoding = encodings[0]
                known_face_encodings.append(encoding)
                known_face_names.append(os.path.splitext(filename)[0])
    return known_face_encodings, known_face_names

known_face_encodings, known_face_names = load_known_faces()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                return jsonify({'error': 'No file part'}), 400
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No selected file'}), 400
            if file and allowed_file(file.filename):
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filename)
                present_students = process_image(filename)
                return jsonify({'present': present_students})
            else:
                return jsonify({'error': 'Invalid file type'}), 400
        except Exception as e:
            app.logger.error(f"An error occurred: {str(e)}")
            
            return jsonify({'error': f'An internal error occurred: {str(e)}'}), 500
    return render_template('upload.html')

def process_image(image_path):
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    present_students = []

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        if True in matches:
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                present_students.append(name)

    mark_attendance(present_students)
    return present_students

def mark_attendance(present_students):
    with open('attendance.csv', 'a') as f:
        for student in present_students:
            now = datetime.now()
            dtString = now.strftime('%Y-%m-%d %H:%M:%S')
            f.writelines(f'\n{student},{dtString}')

if __name__ == '__main__':
    app.run(debug=True)