from flask import Flask, render_template, request, redirect, url_for, send_file
import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import csv
import base64

app = Flask(__name__)

class AttendanceSystem:
    def __init__(self):
        self.known_faces, self.known_names, self.known_reg_numbers = self.load_known_faces("static/imageData")

    def load_known_faces(self, directory):
        known_faces, known_names, known_reg_numbers = [], [], []
        
        for filename in os.listdir(directory):
            if filename.endswith((".jpg", ".jpeg", ".png")):
                image_path = os.path.join(directory, filename)
                name_parts = os.path.splitext(filename)[0].split(".")
                
                name = name_parts[0]
                reg_number = name_parts[1] if len(name_parts) > 1 else "Unknown"
                
                try:
                    image = face_recognition.load_image_file(image_path)
                    encodings = face_recognition.face_encodings(image)
                    if encodings:
                        known_faces.append(encodings[0])
                        known_names.append(name)
                        known_reg_numbers.append(reg_number)
                    else:
                        print(f"No face found in {filename}. Skipping.")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
        
        return known_faces, known_names, known_reg_numbers

    def get_accuracy(self, face_distance, face_match_threshold=0.6):
        if face_distance > face_match_threshold:
            range = (1.0 - face_match_threshold)
            linear_val = (1.0 - face_distance) / (range * 2.0)
            return linear_val
        else:
            range = face_match_threshold
            linear_val = 1.0 - (face_distance / (range * 2.0))
            return linear_val + ((1.0 - linear_val) * np.power((linear_val - 0.5) * 2, 0.2))

    def mark_attendance(self, reg_number, name, class_name):
        filename = f"attendance_{class_name}.csv"
        fieldnames = ['Registration Number', 'Name', 'Class', 'Date', 'Time']
        
        file_exists = os.path.isfile(filename)
        
        try:
            with open(filename, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                
                current_time = datetime.now()
                writer.writerow({
                    'Registration Number': reg_number,
                    'Name': name,
                    'Class': class_name,
                    'Date': current_time.strftime('%Y-%m-%d'),
                    'Time': current_time.strftime('%H:%M:%S')
                })
        except Exception as e:
            print(f"Error marking attendance: {e}")

attendance_system = AttendanceSystem()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_attendance', methods=['POST'])
def start_attendance():
    class_name = request.form['class_name']
    return render_template('attendance.html', class_name=class_name)

@app.route('/process_frame', methods=['POST'])
def process_frame():
    class_name = request.form['class_name']
    image_data = request.form['image_data']
    
    # Decode base64 image
    try:
        image_data = image_data.split(',')[1]
        image_array = np.frombuffer(base64.b64decode(image_data), np.uint8)
        frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    except Exception as e:
        return f"Error processing image data: {e}"

    # Process the frame
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(attendance_system.known_faces, face_encoding)
        face_distances = face_recognition.face_distance(attendance_system.known_faces, face_encoding)
        
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            accuracy = attendance_system.get_accuracy(face_distances[best_match_index]) * 100
            name = attendance_system.known_names[best_match_index]
            reg_number = attendance_system.known_reg_numbers[best_match_index]
            
            if accuracy > 50:
                attendance_system.mark_attendance(reg_number, name, class_name)
                return f"Attendance marked for {name} with {accuracy:.2f}% accuracy"
    
    return "No face recognized with sufficient accuracy"

@app.route('/show_students')
def show_students():
    students = []
    for filename in os.listdir("static/imageData"):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            name_parts = os.path.splitext(filename)[0].split(".")
            name = name_parts[0]
            reg_number = name_parts[1] if len(name_parts) > 1 else "Unknown"
            students.append({
                'name': name,
                'reg_number': reg_number,
                'image_path': f"imageData/{filename}"
            })
    return render_template('students.html', students=students)

@app.route('/view_attendance')
def view_attendance():
    attendance_files = [f for f in os.listdir('.') if f.startswith('attendance_') and f.endswith('.csv')]
    return render_template('view_attendance.html', attendance_files=attendance_files)

@app.route('/download_attendance/<filename>')
def download_attendance(filename):
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Error downloading file: {e}"
    
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        full_name = request.form['full_name']
        father_name = request.form['father_name']
        surname = request.form['surname']
        roll_number = request.form['roll_number']
        image_data = request.form['image_data']
        
        # Create the filename for the student photo
        filename = f"{full_name}.{roll_number}.jpg"
        image_path = os.path.join("static/imageData", filename)
        
        # Decode base64 image and save it
        image_data = image_data.split(',')[1]
        with open(image_path, "wb") as f:
            f.write(base64.b64decode(image_data))
        
        return redirect(url_for('show_students'))  # Redirect to show all students

    return render_template('add_student.html')


if __name__ == '__main__':
    app.run(debug=True)
