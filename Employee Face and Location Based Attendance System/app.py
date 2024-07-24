import cv2
import os
from flask import Flask, request, render_template
from datetime import date, datetime
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import joblib
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from geopy.geocoders import Nominatim
import geopy.distance
import requests

app = Flask(__name__)

nimgs = 10

imgBackground = cv2.imread("C:\\Users\\ELCOT\\Downloads\\face_recognition_flask-main\\face_recognition_flask-main\\background.png")

datetoday = date.today().strftime("%m_%d_%y")
datetoday2 = date.today().strftime("%d-%B-%Y")

face_detector = cv2.CascadeClassifier('C:\\Users\\ELCOT\\Downloads\\face_recognition_flask-main\\face_recognition_flask-main\\haarcascade_frontalface_default.xml')

# Add your Google Sheets credentials JSON file path
CREDENTIALS_FILE = 'C:\\Users\\ELCOT\\Downloads\\face_recognition_flask-main\\face_recognition_flask-main\\tough-ivy-422315-h4-e95dd47b045f.json'

# Add the Google Sheets document key
SPREADSHEET_KEY = '1ynwgc9Yen5LWPMpl-HFMTJ3HiGHH763Ejf8VBRei_mw'

# Define the scope for Google Sheets API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# Initialize geocoder
geolocator = Nominatim(user_agent="your_app_name")

# Google Maps Geocoding API Key
API_KEY = '663725614caf3804153127bkh37e613'

# def geocode_address(address):
#     url = f'https://geocode.maps.co/geocode/json?key={API_KEY}&address={address}'
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         if data['status'] == 'OK':
#             # Extract latitude and longitude from the response
#             latitude = data['results'][0]['geometry']['location']['lat']
#             longitude = data['results'][0]['geometry']['location']['lng']
#             return latitude, longitude
#     return None, None

# def reverse_geocode(latitude, longitude):
#     url = f'https://geocode.maps.co/reverse?lat={latitude}&lng={longitude}&api_key={API_KEY}'
    
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         data = response.json()

#         if data.get('status') == 'OK':
#             # Extract the formatted address from the response
#             formatted_address = data.get('results', [{}])[0].get('formatted_address')
#             return formatted_address
#         else:
#             print("Reverse geocoding request failed. Status:", data.get('status'))

#     except requests.RequestException as e:
#         print("Error making the request:", e)

#     return None
# # Authenticate and authorize using credentials
# creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
# client = gspread.authorize(creds)
# sheet = client.open_by_key(SPREADSHEET_KEY).sheet1

# if not os.path.isdir('static'):
#     os.makedirs('static')
# if not os.path.isdir('static/faces'):
#     os.makedirs('static/faces')
# if f'Attendance-{datetoday}.csv' not in os.listdir('Attendance'):
#     with open(f'Attendance/Attendance-{datetoday}.csv', 'w') as f:
#         f.write('Name,Roll,Time,Location')


def totalreg():
    return len(os.listdir('static/faces'))


def extract_faces(img):
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_points = face_detector.detectMultiScale(gray, 1.2, 5, minSize=(20, 20))
        return face_points
    except:
        return []


def identify_face(facearray):
    model = joblib.load('static/face_recognition_model.pkl')
    return model.predict(facearray)


def train_model():
    faces = []
    labels = []
    userlist = os.listdir('static/faces')
    for user in userlist:
        for imgname in os.listdir(f'static/faces/{user}'):
            img = cv2.imread(f'static/faces/{user}/{imgname}')
            resized_face = cv2.resize(img, (50, 50))
            faces.append(resized_face.ravel())
            labels.append(user)
    faces = np.array(faces)
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(faces, labels)
    joblib.dump(knn, 'static/face_recognition_model.pkl')


# def add_attendance(name):
#     username = name.split('_')[0]
#     userid = name.split('_')[1]
#     current_time = datetime.now().strftime("%H:%M:%S")
    
#     # Get current location (latitude, longitude)
#     location = geolocator.geocode("User's location")
    
#     # Geocode the address to obtain latitude and longitude
#     latitude, longitude = geocode_address(location)
    
#     # Print the location object for debugging
#     print("Location:", location)
    
#     # Check if location is successfully retrieved
#     if latitude is not None and longitude is not None:
#         location_name = f"{latitude}, {longitude}"
#     else:
#         location_name = "not in office"
    
#     # Append data to Google Sheets
#     new_row = [username, userid, current_time, location_name]
#     print("Adding attendance:", new_row)  # Debug print
#     sheet.append_row(new_row)
# def add_attendance(name):
#     username = name.split('_')[0]
#     userid = name.split('_')[1]
#     current_time = datetime.now().strftime("%H:%M:%S")
    
#     # Get current location (latitude, longitude)
#     geolocator = Nominatim(user_agent="geoapiExercises")
#     location = geolocator.geocode("User's location")

#     if location:
#         latitude = location.latitude
#         longitude = location.longitude

#         # Reverse geocode the coordinates to obtain address
#         location_name = reverse_geocode(latitude, longitude)
        
#         # Check if location name is retrieved successfully
#         if location_name is None:
#             location_name = "Unknown Location"
        
#         # Append data to Google Sheets
#         new_row = [username, userid, current_time, location_name]
#         print("Adding attendance:", new_row)  # Debug print
#         sheet.append_row(new_row)  # Assuming 'sheet' is the Google Sheets object
#     else:
#         print("Unable to retrieve current location.")
def add_attendance_to_sheet(name, userid, latitude, longitude):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('face_recognition_flask-main\\face_recognition_flask-main\\tough-ivy-422315-h4-e95dd47b045f.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key('1ynwgc9Yen5LWPMpl-HFMTJ3HiGHH763Ejf8VBRei_mw').sheet1
    current_time = datetime.now().strftime("%H:%M:%S")
    office_latitude = 17.3724246  # Replace with your office latitude
    office_longitude =  78.4378789# Replace with your office longitude

    # Check if user is in office
    if abs(latitude - office_latitude) < 0.01 and abs(longitude - office_longitude) < 0.01:
        location_status = "In Office"
    else:
        location_status = "Not In Office"
    row = [name, userid,current_time, latitude, longitude,location_status]
    sheet.append_row(row)
def get_location_by_ip():
    # Get public IP address
    public_ip = requests.get('https://api.ipify.org').text

    # Use ip-api to get location by IP
    response = requests.get(f'http://ip-api.com/json/{public_ip}')

    if response.status_code == 200:
        data = response.json()
        return data['lat'], data['lon']
    else:
        print("Unable to retrieve current location.")
        return None, None

latitude, longitude = get_location_by_ip()
if latitude and longitude:
    print(f"Latitude: {latitude}, Longitude: {longitude}")
def add_attendance(name):
    username = name.split('_')[0]
    userid = name.split('_')[1]
    current_time = datetime.now().strftime("%H:%M:%S")
    
    # Get current location (latitude, longitude)
    latitude, longitude = get_location_by_ip()
    if latitude and longitude:
        # Append data to Google Sheets
        new_row = [username, userid, current_time, latitude, longitude]
        print("Adding attendance:", new_row)  # Debug print
        add_attendance_to_sheet(username,userid, latitude, longitude)
    else:
        print("Unable to retrieve current location.")


def extract_attendance():
    try:
        df = pd.read_csv(f'Attendance/Attendance-{datetoday}.csv')
        names = df['Name']
        rolls = df['Roll']
        times = df['Time']
        locations = df['Location']
        l = len(df)
    except KeyError:
        # If 'Location' column is not present, assign an empty list
        names, rolls, times, locations, l = [], [], [], [], 0
    return names, rolls, times, locations, l



def getallusers():
    userlist = os.listdir('static/faces')
    names = []
    rolls = []
    l = len(userlist)

    for i in userlist:
        name, roll = i.split('_')
        names.append(name)
        rolls.append(roll)

    return userlist, names, rolls, l


@app.route('/')
def home():
    names, rolls, times, locations, l = extract_attendance()
    return render_template('home.html', names=names, rolls=rolls, times=times, locations=locations, l=l, totalreg=totalreg(),
                           datetoday2=datetoday2)


@app.route('/start', methods=['GET'])
def start():
    names, rolls, times, locations, l = extract_attendance()

    if 'face_recognition_model.pkl' not in os.listdir('static'):
        return render_template('home.html', names=names, rolls=rolls, times=times, locations=locations, l=l, totalreg=totalreg(),
                               datetoday2=datetoday2,
                               mess='There is no trained model in the static folder. Please add a new face to continue.')

    ret = True
    cap = cv2.VideoCapture(0)
    while ret:
        ret, frame = cap.read()
        if len(extract_faces(frame)) > 0:
            (x, y, w, h) = extract_faces(frame)[0]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (86, 32, 251), 1)
            cv2.rectangle(frame, (x, y), (x + w, y - 40), (86, 32, 251), -1)
            face = cv2.resize(frame[y:y + h, x:x + w], (50, 50))
            identified_person = identify_face(face.reshape(1, -1))[0]
            
            # Add attendance
            add_attendance(identified_person)
            
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
            cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
            cv2.putText(frame, f'{identified_person}', (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)
            break  # Exit loop after detecting a face
        imgBackground[162:162 + 480, 55:55 + 640] = frame
        cv2.imshow('Attendance', imgBackground)
        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    names, rolls, times, locations, l = extract_attendance()
    return render_template('home.html', names=names, rolls=rolls, times=times, locations=locations, l=l, totalreg=totalreg(),
                           datetoday2=datetoday2, mess='Attendance marked')


@app.route('/add', methods=['GET', 'POST'])
def add():
    newusername = request.form['newusername']
    newuserid = request.form['newuserid']
    userimagefolder = 'static/faces/' + newusername + '_' + str(newuserid)
    if not os.path.isdir(userimagefolder):
        os.makedirs(userimagefolder)
    i, j = 0, 0
    cap = cv2.VideoCapture(0)
    while 1:
        _, frame = cap.read()
        faces = extract_faces(frame)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 20), 2)
            cv2.putText(frame, f'Images Captured: {i}/{nimgs}', (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 20), 2, cv2.LINE_AA)
            if j % 5 == 0:
                name = newusername + '_' + str(i) + '.jpg'
                cv2.imwrite(userimagefolder + '/' + name, frame[y:y + h, x:x + w])
                i += 1
            j += 1
        if j == nimgs * 5:
            break
        cv2.imshow('Adding new User', frame)
        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    print('Training Model')
    train_model()
    names, rolls, times, locations, l = extract_attendance()
    return render_template('home.html', names=names, rolls=rolls, times=times, locations=locations, l=l, totalreg=totalreg(),
                           datetoday2=datetoday2, mess='New user added successfully')


if __name__ == '__main__':
    app.run(debug=True)
