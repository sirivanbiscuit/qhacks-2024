import cv2
import dlib

import face_recognition


class RecogManager:
    
    def __init__(self):
        self.known_faces = {}
        self.add_known("Owen", "scripts/imgs/img1.jpg")
        
    def add_known(self, name, path):
        image = face_recognition.load_image_file(path)
        self.known_faces[name] = \
            face_recognition.face_encodings(image)[0]
    
    def recog_face(self, path):
        u_image = face_recognition.load_image_file(path)
        u_enc = face_recognition.face_encodings(u_image)
        if not u_enc: return 'This is not a person'
        for name, enc in self.known_faces.items():
            matches = face_recognition.compare_faces([enc], u_enc[0])
            if all(matches): return f'This is a picture of {name}'
        return 'This is a person, but they aren\'t recognized'


if __name__=="__main__":
    manager = RecogManager()
    test_path = "scripts/imgs/img4.jpg"
    result = manager.recog_face(test_path)
    print(result)
    