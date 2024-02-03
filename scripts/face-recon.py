import cv2
import tkinter as tk
from PIL import Image, ImageTk

class FaceDetectionApp:
    def __init__(self, root, video_source=0):
        self.root = root
        self.root.title("Face Detection App")

        self.video_source = video_source
        self.video_capture = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(root)
        self.canvas.pack()

        self.btn_quit = tk.Button(root, text="Quit", command=self.quit)
        self.btn_quit.pack()

        self.update()

    def update(self):
        ret, frame = self.video_capture.read()
        if ret:
            self.photo = self.convert_to_tkinter_image(frame)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        self.root.after(10, self.update)

    def convert_to_tkinter_image(self, frame):
        b, g, r = cv2.split(frame)
        img = cv2.merge((r, g, b))
        img = Image.fromarray(img)
        photo = ImageTk.PhotoImage(image=img)
        return photo

    def quit(self):
        self.video_capture.release()
        self.root.destroy()

def detect_and_display_face(video_capture):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # Convert the captured frame to grayscale
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Perform face detection
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Create a Tkinter window
root = tk.Tk()

# Create an instance of the FaceDetectionApp class
app = FaceDetectionApp(root)

try:
    detect_and_display_face(app.video_capture)
finally:
    # When everything is done, release the capture and close the window
    app.video_capture.release()
    cv2.destroyAllWindows()

# Run the Tkinter event loop
root.mainloop()
