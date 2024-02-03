import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class WebcamApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.video_source = 0  # Use the default webcam (change if needed)
        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.label = ttk.Label(window, text="Enter your text:")
        self.label.pack()

        self.entry = ttk.Entry(window)
        self.entry.pack()

        self.btn_capture = ttk.Button(window, text="Capture", command=self.capture)
        self.btn_capture.pack()

        self.btn_exit = ttk.Button(window, text="Exit", command=self.exit_app)
        self.btn_exit.pack()

        self.is_capturing = False
        self.update()
        self.window.mainloop()

    def capture(self):
        text = self.entry.get()
        print(f"Captured text: {text}")

    def exit_app(self):
        if self.is_capturing:
            self.is_capturing = False
        self.vid.release()
        self.window.destroy()

    def update(self):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Capture frame-by-frame
        ret, frame = self.vid.read()

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

        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(10, self.update)

    def start_capturing(self):
        self.is_capturing = True

if __name__ == "__main__":
    root = tk.Tk()
    app = WebcamApp(root, "Webcam App")