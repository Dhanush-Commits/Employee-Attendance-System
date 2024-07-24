# Face Recognition Attendance System

**Step 1: Clone the Repository**
If you haven't already, clone your project repository from GitHub:

git clone https://github.com/yourusername/face-recognition-attendance.git
cd face-recognition-attendance

**Step 2: Create requirements.txt File**

Create a file named requirements.txt in the root directory of your project and add the following content:

Flask==2.2.2
numpy==1.23.1
opencv-python==4.5.4.60
pandas==1.4.3
scikit-learn==1.1.1
joblib==1.1.0
gspread==5.3.2
oauth2client==4.1.3
geopy==2.2.0
requests==2.28.1
Step 3: Install Dependencies
Install the dependencies listed in requirements.txt:

pip install -r requirements.txt

**Step 4: Download Haar Cascade for Face Detection**
Download the haarcascade_frontalface_default.xml file from the OpenCV GitHub repository and place it in the root directory of your project.

**Step 5: Google Sheets Integration**
Credentials JSON File: Place your Google Sheets credentials JSON file in the root directory of your project.
Update Code: Ensure the CREDENTIALS_FILE and SPREADSHEET_KEY variables in your code point to the correct credentials file and spreadsheet key.

**Step 6: Run the Application**
Run your Flask application:


**Step 7: Adding a New User**
Open your web browser and navigate to http://127.0.0.1:5000/add.
Enter the new user's name and ID.
Follow the instructions to capture the user's face using the webcam.
**Step 8: Marking Attendance**
Open your web browser and navigate to http://127.0.0.1:5000/start.
The system will detect and recognize faces, logging attendance with time and location details.


