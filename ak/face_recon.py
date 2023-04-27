import cv2
import numpy as np
import face_recognition

# Load images from directory
known_faces = []
known_names = []
for filename in ["john.jpg", "jane.jpg"]:
    image = face_recognition.load_image_file(filename)
    encoding = face_recognition.face_encodings(image)[0]
    known_faces.append(encoding)
    known_names.append(filename.split(".")[0])

# Capture video from webcam
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
# Convert frame to RGB for face_recognition library
rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Detect faces in the frame
face_locations = face_recognition.face_locations(rgb_frame)
face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

for face_encoding in face_encodings:
    # Compare the detected face encoding with the known face encodings
    matches = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.6)
    name = "Unknown"
    if True in matches:
        # Find the index of the matched face
        match_index = np.argmax(matches)
        name = known_names[match_index]
    # Draw bounding box and label on the frame
    top, right, bottom, left = face_locations
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

# Display the processed frame
cv2.imshow("Face Recognition", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
