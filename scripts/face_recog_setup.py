import os
from cv2 import *
import face_recognition
from cv2 import VideoCapture, imshow, imwrite, waitKey, destroyWindow


class RecogManager:

    def __init__(self):
        self.known_faces = {}
        self.add_known("Owen", r"C:\Users\david\PycharmProjects\qhacks-2024\scripts\imgs\img1.jpg")

    def add_known(self, name, path):
        image = face_recognition.load_image_file(path)
        self.known_faces[name] = face_recognition.face_encodings(image)[0]

    def recog_face(self, path):
        u_image = face_recognition.load_image_file(path)
        u_enc = face_recognition.face_encodings(u_image)
        if not u_enc:
            return 'This is not a person'
        for name, enc in self.known_faces.items():
            matches = face_recognition.compare_faces([enc], u_enc[0])
            if all(matches):
                return f'This is a picture of {name}'
        return 'This is a person, but not Owen'

def capture_and_save_image():
    # Open a connection to the webcam
    cam = VideoCapture(0)
    result, image = cam.read()

    # If image is detected without any error, show result
    if result:
        # Display the image
        imshow("Image Taker", image)

        # Prompt user for a name
        user_input_name = input("Enter a name for the image: ")

        # Construct the filename
        filename = f"{user_input_name}.png"
        count = 1

        # Check if the file already exists, if yes, append a number
        while os.path.exists(filename):
            filename = f"imgs/{user_input_name}{count}.png"
            count += 1

        # Save the image with the unique filename
        imwrite(filename, image)
        print(f"Image saved as {filename}")

        # Close the image window when x button is clicked
        key = waitKey(0)
        if key == 27:  # 27 corresponds to the ASCII value of the escape key
            destroyWindow("Image Taker")

    else:
        print("No image detected. Please try again")

if __name__ == "__main__":
    # Capture and save image
    capture_and_save_image()

    # Face recognition test
    manager = RecogManager()
    test_path = r"C:\Users\david\PycharmProjects\qhacks-2024\scripts\imgs\img4.jpg"
    result = manager.recog_face(test_path)
    print(result)
