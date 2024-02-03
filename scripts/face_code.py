"""
This is a basic program that will only close when you scan
a picture of the correct person's face. The current face
reference is stored at scripts/code/passcode.png
"""

import cv2
import face_recognition
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk

# put image paths here
CACHE_INFO = 'scripts/scans/cache/cache_info.txt'
CACHE_PREF = 'scripts/scans/cache/img_'
PASSCODE = 'scripts/scans/passcode.jpg'


"""
Frame that holds the webcam preview and a button to scan
your face. The scan button will send an image to the cache
at scripts/code/cache and compare it with the code.
"""
class FaceCodeApp:
    
    def __init__(self, win, title):
        # window info
        self.win = win
        self.win.title(title)
        self.vid = cv2.VideoCapture(0)
        # canvas structure
        self.canvas = tk.Canvas(
            win, 
            width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), 
            height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.scan = tk.Button(
            win, 
            text="Scan Face",
            command=self.scan_face,
            height=2,
            font=("Arial", 12, "bold")
            )
        # packing
        self.canvas.pack()
        self.scan.pack(fill=tk.X, expand=True)
        # cascade
        self.casc = cv2.CascadeClassifier(
            'C:/Users/siriv/Documents/QHacks 2024/repo/qhacks-2024/scripts/xml/haarcascade_frontalface_default.xml'
            )
        # running
        self.update()
        self.win.mainloop()
    
    def scan_face(self):
        # get id from cache
        cache_id = None
        with open(CACHE_INFO, 'r') as file: cache_id = int(file.read())
        # save webcam shot to cache
        get, image = self.vid.read()
        path = f'{CACHE_PREF}{cache_id}.png'
        if get: cv2.imwrite(path, image)
        with open(CACHE_INFO, 'w') as file: file.write(str(cache_id+1))
        # check valid face id
        man = RecogManager()
        if man.recog_face(path): 
            self.win.destroy()
            print('Passed user indentification')
        else: 
            self.scan.config(fg='red')
            print('Failed user indentification')
    
    def update(self):
        # setup frame recieval
        get, frame = self.vid.read()
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.casc.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(30, 30), 
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        # find faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # print webcam image
        if get:
            self.photo = ImageTk.PhotoImage(
                image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                )
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        # recursively call a new update
        self.win.after(10, self.update)


"""
Compares an input image with the code image to check if they
are of the same person.
"""
class RecogManager:

    def __init__(self):
        self.known_faces = {}
        self.add_known("user", PASSCODE)

    def add_known(self, name, path):
        image = face_recognition.load_image_file(path)
        self.known_faces[name] = face_recognition.face_encodings(image)[0]

    def recog_face(self, path):
        u_image = face_recognition.load_image_file(path)
        u_enc = face_recognition.face_encodings(u_image)
        if not u_enc:
            return None
        for name, enc in self.known_faces.items():
            matches = face_recognition.compare_faces([enc], u_enc[0])
            if all(matches): return 1
        return 0
    
    
"""
Execute the program frame
"""
if __name__=="__main__": 
    app = FaceCodeApp(tk.Tk(), "Face Code Test")
        