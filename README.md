# Face Recognition Attendance System

## Overview
This project is a face recognition-based attendance system implemented using Flask, OpenCV, and machine learning techniques. It captures faces, recognizes them, and marks attendance with details like time and location.

## Features
- Face detection using OpenCV's Haar cascades.
- Face recognition using K-Nearest Neighbors (KNN) classifier.
- Attendance logging with time and geolocation.
- Integration with Google Sheets for storing attendance records.
- Web interface built with Flask.

## Technologies Used
- Python
- Flask
- OpenCV
- Scikit-learn
- Pandas
- Joblib
- GSpread
- OAuth2Client
- Geopy
- Requests

## Project Structure
project_root\
├── static\
│   ├── faces\
│   │   └── (image files for faces, if any)\
│   ├── face_recognition_model.pkl\
│   └── background.png\
├── templates\
│   └── home.html\
├── Attendance\
│   └── Attendance-.csv\
├── app.py\
├── haarcascade_frontalface_default.xml\
├── requirements.txt\
└── README.md


## Setup Instructions

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/face-recognition-attendance.git
    cd face-recognition-attendance
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Download Haar Cascade for face detection:**
    Download the `haarcascade_frontalface_default.xml` file from [OpenCV GitHub](https://github.com/opencv/opencv/tree/master/data/haarcascades) and place it in the project root.

4. **Google Sheets Integration:**
    - Add your Google Sheets credentials JSON file and update the `CREDENTIALS_FILE` and `SPREADSHEET_KEY` in the code.
    - Make sure the Google Sheets API is enabled and the credentials are correct.

5. **Run the application:**
    ```bash
    python app.py
    ```

## Usage

### Adding a New User
1. Navigate to the `/add` route in your browser.
2. Enter the new user's name and ID.
3. Capture the user's face using the webcam.
4. The system will train the model and add the new user.

### Marking Attendance
1. Navigate to the `/start` route in your browser.
2. The system will use the webcam to detect and recognize faces.
3. Attendance will be logged with time and location details.

## Contributions
Contributions are welcome! Please fork the repository and submit a pull request for any improvements or new features.

## License
This project is licensed under the MIT License.


