from cryptography.fernet import Fernet
#from encode_decode import encode,decode,writeFile
import PySimpleGUI as sg
import os
import shutil
import cv2
from PIL import Image, ImageTk

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
def decrypt_from_exe(exe_path):
    # Read the encrypted data from the executable
    with open(exe_path, 'rb') as exe_file:
        encrypted_data = exe_file.read()
    print(exe_path)
    # Ask for validation statement
   # user_input = input("Enter the validation statement: ")
    
    #Change here to allow for face == true
   # if user_input != "yes":
   #     print("Validation failed. Exiting.")
   #    return

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
        [sg.Text('Take an image of yourself:'), sg.Button('Show webcam', key='t_cam')],
        [sg.Image(filename='', key='webcam')],
        [sg.Button('Take Image', key='img', disabled=True), 
         sg.Button('Reset', key='reset', disabled=True)],
        [sg.Text('Select a file to encrypt:')],
        [sg.InputText(key='file_path'), sg.FileBrowse()],
        [sg.Button('Encrypt to EXE', key='enc'), sg.Button('Decrypt from EXE', key='dec')]
    ]

    window = sg.Window('File Encryptor', layout)
    vid = cv2.VideoCapture(0)
    casc = cv2.CascadeClassifier(CASC)
    cam_img = None
    freeze_img = False
    hide_cam = True
    

    while True:
        event, values = window.read(timeout=20)
        
        if event == 't_cam':
            if 'Show' in window['t_cam'].get_text():
                window['t_cam'].update('Hide webcam')
                window['img'].update(disabled=False)
                window['reset'].update(disabled=True)
                freeze_img=False
                hide_cam=False
            else:
                window['t_cam'].update('Show webcam')
                window['img'].update(disabled=True)
                window['reset'].update(disabled=True)
                hide_cam=True
                
        
        if event in (sg.WIN_CLOSED, 'Exit'): break
        
        if event == 'img':
            # get id from cache
            cache_id = None
            with open(CACHE_INFO, 'r') as file: cache_id = int(file.read())
            # save webcam shot to cache
            get, image = vid.read()
            path = f'{CACHE_PREF}{cache_id}.png'
            if get: cv2.imwrite(path, image)
            with open(CACHE_INFO, 'w') as file: file.write(str(cache_id+1))
            cam_img=path
            freeze_img=True
            window['img'].update(disabled=True)
            window['reset'].update(disabled=False)
        
        if event == 'reset':
            freeze_img=False
            window['img'].update(disabled=False)
            window['reset'].update(disabled=True)
        
        ret, frame = vid.read()
        faces = []
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
        
        if not hide_cam:
            if not freeze_img: window['webcam'].update(
                data=cv2.imencode('.png', frame)[1].tobytes()
                )
        else:
            window['webcam'].update(data=None)
            
        if event == 'img':
            # get id from cache
            cache_id = None
            with open(CACHE_INFO, 'r') as file: cache_id = int(file.read())
            # save webcam shot to cache
            get, image = vid.read()
            path = f'{CACHE_PREF}{cache_id}.png'
            if get: cv2.imwrite(path, image)
            with open(CACHE_INFO, 'w') as file: file.write(str(cache_id+1))
            cam_img=path

        if event == sg.WIN_CLOSED:
            break
        elif event == 'enc':
            file_path = values['file_path']
            if file_path:
                exe_path = encrypt_to_exe(file_path)
                sg.popup(f'File encrypted and saved as {exe_path}')
        elif event == 'dec':
            file_path = values['file_path']
            #if file_path:
               # validation_statement = sg.popup_get_text('Enter validation statement:')
                #if validation_statement:
            decrypt_from_exe(file_path)

    vid.release()
    window.close()


if __name__ == '__main__':
    main()
