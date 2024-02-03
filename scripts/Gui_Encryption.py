from cryptography.fernet import Fernet
import PySimpleGUI as sg
import os
import shutil
import cv2
from PIL import Image, ImageTk
import face_recognition

# put image paths here
CACHE_INFO = 'res/scans/cache/cache_info.txt'
CACHE_PREF = 'res/scans/cache/img_'
PASSCODE = 'res/scans/passcode.jpg'
CASC = 'res/xml/haarcascade_frontalface_default.xml'

#hi
# Function to encrypt a file into an executable
def encrypt_to_exe(file_path):
    # Generate a key for encryption
    key = Fernet.generate_key()
    cipher = Fernet(key)

    # Read the file content
    with open(file_path, 'rb') as file:
        data = file.read()

    # Encrypt the file content
    encrypted_data = cipher.encrypt(data)

    # Create a new executable file with encrypted data
    exe_path = file_path + '.exe'
    with open(exe_path, 'wb') as exe_file:
        exe_file.write(encrypted_data)

    # Remove the original file
    os.remove(file_path)

    return exe_path

# Function to decrypt an executable file with a validation statement
def decrypt_from_exe(exe_path, validation_statement):
    # Read the encrypted data from the executable
    with open(exe_path, 'rb') as exe_file:
        encrypted_data = exe_file.read()

    # Ask for validation statement
    user_input = input("Enter the validation statement: ")
    #Change here to allow for face == true
    if user_input != validation_statement:
        print("Validation failed. Exiting.")
        return

    # Decrypt the data using the stored key
    key = Fernet.generate_key()
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data)

    # Get the original file path
    file_path = os.path.splitext(exe_path)[0]

    # Write the decrypted data back to the original file
    with open(file_path, 'wb') as file:
        file.write(decrypted_data)

    # Remove the executable file
    os.remove(exe_path)


# Example usage with a simple GUI for file path input
def main():
    sg.theme('Default1')

    layout = [
        [sg.Text('Take an image of yourself:')],
        [sg.Image(filename='', key='-IMAGE-')],
        [sg.Text('Select a file to encrypt:')],
        [sg.InputText(key='file_path'), sg.FileBrowse()],
        [sg.Button('Encrypt to EXE'), sg.Button('Decrypt from EXE')]
    ]

    window = sg.Window('File Encryptor', layout)
    vid = cv2.VideoCapture(0)
    casc = cv2.CascadeClassifier(CASC)

    while True:
        event, values = window.read(timeout=20)
        
        if event in (sg.WIN_CLOSED, 'Exit'): break
        
        ret, frame = vid.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = casc.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(30, 30), 
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        # find faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
        window['-IMAGE-'].update(
            data=cv2.imencode('.png', frame)[1].tobytes()
            )

        if event == sg.WIN_CLOSED:
            break
        elif event == 'Encrypt to EXE':
            file_path = values['file_path']
            if file_path:
                exe_path = encrypt_to_exe(file_path)
                sg.popup(f'File encrypted and saved as {exe_path}')
        elif event == 'Decrypt from EXE':
            file_path = values['file_path']
            if file_path:
                validation_statement = sg.popup_get_text('Enter validation statement:')
                if validation_statement:
                    decrypt_from_exe(file_path, validation_statement)

    vid.release()
    window.close()
    
    
def update(self, vid, casc):
        # setup frame recieval
        get, frame = vid.read()
        frame = cv2.flip(frame, 1)
        
        # print webcam image
        if get:
            photo = ImageTk.PhotoImage(
                image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                )
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        # recursively call a new update
        self.win.after(10, self.update)


if __name__ == '__main__':
    main()
