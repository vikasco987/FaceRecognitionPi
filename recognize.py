import cv2
import face_recognition
import pickle
import time
import os

encodings_path = "encodings.pickle"
attendance_log = "attendance_log.txt"

with open(encodings_path, "rb") as f:
    data = pickle.load(f)

cap = cv2.VideoCapture(0)
print("[INFO] Starting recognition. Press 'q' to quit.")

logged_names = set()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, boxes)

    for encoding, box in zip(encodings, boxes):
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"

        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            for i in matchedIdxs:
                matched_name = data["names"][i]
                counts[matched_name] = counts.get(matched_name, 0) + 1

            name = max(counts, key=counts.get)

            # Log attendance once per session
            if name not in logged_names:
                logged_names.add(name)
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                with open(attendance_log, "a") as f:
                    f.write(f"{timestamp} - {name}\n")
                print(f"[LOGGED] {name} at {timestamp}")

        top, right, bottom, left = box
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
