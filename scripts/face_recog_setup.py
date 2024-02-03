import cv2

class RecogManager:
    
    def __init__(self, path):
        self.face_casc = cv2.CascadeClassifier