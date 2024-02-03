import cv2

def detect_and_display_face(video_capture):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # Convert the captured frame to grayscale
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        font = cv2.FONT_HERSHEY_PLAIN

        # Perform face detection
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.putText(frame, 'hello', (x,y), font,0.9, (0, 255, 0))
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Start video capture from the default webcam (index 0)
video_capture = cv2.VideoCapture(0)

try:
    detect_and_display_face(video_capture)
finally:
    # When everything is done, release the capture and close the window
    video_capture.release()
    cv2.destroyAllWindows()