
# Facial Recognition-Based Attendance System

This project is a **Facial Recognition-Based Attendance System** that automates attendance marking using computer vision. The system captures live images or video feed, detects faces, and matches them with a pre-trained facial dataset. Once a match is identified, the system records the attendance, offering an efficient, contactless solution ideal for environments like classrooms, offices, or events.

### Key Features:
- **Real-time Face Detection**: The system uses OpenCV to detect faces in real-time from a camera feed or images.
- **Facial Recognition**: It utilizes pre-trained models such as `face_recognition` or `dlib` to match detected faces with stored user data.
- **Automated Attendance Logging**: Upon successful face recognition, the attendance is logged automatically, and records can be stored in a database (e.g., SQLite, MySQL) or CSV file.
- **Easy Enrollment**: Users can register their facial data by uploading images or capturing them through a webcam.
- **Customizable**: The system is flexible, allowing you to expand it with more cameras and scale the dataset for larger environments.

### Technologies:
- **Python** for the core logic.
- **OpenCV** for image processing and real-time face detection.
- **face_recognition** library for accurate face matching.
- **Flask/Django** (optional) for creating a web interface.
- **SQLite/MySQL** for attendance record storage.

### How It Works:
1. Add users by capturing and storing their facial images.
2. The system processes real-time video or image feeds, detects faces, and compares them to the stored dataset.
3. When a match is found, the attendance for that individual is automatically logged.
4. Attendance reports can be generated and viewed in the system or exported as needed.

   ## Result & Discussion
- This method can **detect multiple face** in one frame and can be easily used in a classroom or in an office.
- This system helps us to achieve desired results with **better accuracy** and less time consumption.
- The precision or the accuracy of face recognition of our model is almost **more than 90%**.

## Conclusion
Thus, the aim of this model is to capture the video of the
students/colleagues, convert it into frames, relate it with the dataset to
ensure their presence or absence, mark attendance to the
particular student/colleagues to maintain the record. The Automated
Classroom Attendance System helps in increasing the
accuracy and speed ultimately achieve the high-precision
real-time attendance to meet the need for automatic
classroom evaluation.

## Steps to Run
1. Fork this repo
2. Clone the forked repo to your local system
3. Install the following libraries: (in **Linux** or **macOS**)
   1. `cv2`
   2. `face_recogniton`
   3. `os`
   4. `math`
   5. `numpy`
   6. `datetime`
4. Add your image inside `imageData` folder in **format** -> `name.registration.jpg`, if adding more than one image of same person then **format** -> `name.registration.(0,1,2).jpg`, only after that it will recognize you. 
5. Run the code -> `app.py`
6. If it will recognise you, your attendance will be there in `Attendance.csv` file
7. If you have a existing photo of class then run 'python mul.py' in the terminal and upload the photo from uploads folder and get attendance.

**(Provide more than one image with different angle to get more accuracy)**


