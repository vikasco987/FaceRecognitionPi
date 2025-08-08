import cv2
import face_recognition
import pymongo
from datetime import datetime

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["attendance"]
collection = db["records"]

# Load known face images and encode
known_faces = []
known_names = []
known_emails = []

# Add known users
# 👇 Add as many as needed (image must be in same folder)
known_users = [
    {"name": "Shubham", "email": "shubham@example.com", "image": "shubham.jpg"},
    {"name": "Sankar", "email": "sankar@example.com", "image": "sankar.jpg"},
    {"name": "Rahul", "email": "rahul@example.com", "image": "rahul.jpg"},
]

for user in known_users:
    image = face_recognition.load_image_file(user["image"])
    encoding = face_recognition.face_encodings(image)[0]
    known_faces.append(encoding)
    known_names.append(user["name"])
    known_emails.append(user["email"])

# Start webcam
video_capture = cv2.VideoCapture(0)
print("[INFO] Starting camera...")

while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        name = "Unknown"
        email = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]
            email = known_emails[first_match_index]

            now = datetime.now()
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")

            # Check if already marked today
            existing = collection.find_one({
                "name": name,
                "date": now.strftime("%Y-%m-%d")
            })

            if not existing:
                collection.insert_one({
                    "name": name,
                    "email": email,
                    "date": now.strftime("%Y-%m-%d"),
                    "time": now.strftime("%H:%M:%S")
                })
                print(f"[ATTENDANCE] Marked for {name} at {date_time}")

        else:
            print("[WARNING] Unknown face detected")

    # Display video
    cv2.imshow('Attendance Camera', frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
