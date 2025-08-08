import cv2
import os
import pymongo
from datetime import datetime

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["face_attendance"]
users_collection = db["users"]

# Get user input
name = input("Enter your full name: ").strip()
email = input("Enter your email: ").strip()

# Save user info to MongoDB
user_data = {
    "name": name,
    "email": email,
    "created_at": datetime.now().isoformat()
}
user_id = users_collection.insert_one(user_data).inserted_id
print(f"[INFO] User {name} registered with ID: {user_id}")

# Create dataset directory for the user
dataset_path = "dataset"
user_path = os.path.join(dataset_path, str(user_id))
os.makedirs(user_path, exist_ok=True)

# Open camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[ERROR] Could not access the camera.")
    exit()

# Load Haarcascade
face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(face_cascade_path)
if face_cascade.empty():
    print("[ERROR] Failed to load Haarcascade.")
    exit()

count = 0
max_images = 100

print(f"[INFO] Capturing images for {name}. Please look at the camera.")
print("[INFO] Press 'q' to quit early.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] Failed to grab frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        count += 1
        face_img = frame[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (200, 200))  # Normalize size
        img_path = os.path.join(user_path, f"{count}.jpg")
        cv2.imwrite(img_path, face_img)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"Captured {count}/{max_images}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        if count >= max_images:
            break

    cv2.imshow("Registering Face", frame)

    if cv2.waitKey(1) & 0xFF == ord('q') or count >= max_images:
        break

cap.release()
cv2.destroyAllWindows()

print(f"[INFO] Registration complete! {count} images saved to: {user_path}")
