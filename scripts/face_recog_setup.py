import cv2

class RecogManager:
    
    def __init__(self, path='xml/haarcascade_frontalface_default.xml'):
        self.face_casc = cv2.CascadeClassifier(path)
    
    def recog(self, path):
        img = cv2.imread(path)
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        face_find = self.face_casc.detectMultiScale(
            grey, 
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30,30)
            )
        
        return not len(face_find)


if __name__=="__main__":
    manager = RecogManager()
    