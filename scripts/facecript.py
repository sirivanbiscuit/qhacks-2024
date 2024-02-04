from cryptography.fernet import Fernet
import PySimpleGUI as sg
import os
import cv2
from util.enc_dec import encode_png, decode_png
from util.face_utils import faceFromPath


# put image paths here
CACHE_INFO = 'res/cache/cache_info.txt'
CACHE_PREF = 'res/cache/img_'
CASC = 'res/xml/haarcascade_frontalface_default.xml'
SAVE_XML = 'res/xml/'


#hi
# Function to encrypt a file into an executable
def encrypt_file(file_path, img_path):
    # Generate a key for encryption
    #key = Fernet.generate_key()
    #with open("filekey.key", "wb") as f:  # Change to 'wb' to write bytes
        #f.write(key)

    key = None
    with open("filekey.key", "rb") as f:  # Read the key
        key = f.read()

    cipher = Fernet(key)

    # Read the file content
    with open(file_path, 'rb') as file:
        data = file.read()

    # Encrypt the file content
    encrypted_data = cipher.encrypt(data)
    encoded_img = encode_png(img_path)

    # Create a new file with encrypted data, without adding '.exe' extension
    encrypted_file_path = file_path + '.encrypted'
    with open(encrypted_file_path, 'w') as encrypted_file:
        encrypted_file.write(encoded_img)
    with open(encrypted_file_path, 'a') as encrypted_file:
        encrypted_file.write('\n')   
    with open(encrypted_file_path, 'ab') as encrypted_file:
        encrypted_file.write(encrypted_data)
    

    # Remove the original file
    os.remove(file_path)

    return encrypted_file_path


# Function to decrypt an executable file with a validation statement
def decrypt_file(encrypted_file_path, img_attempt_path):
    layout = [[sg.Text("Enter the validation statement:")],
              [sg.InputText()],
              [sg.Button('Submit'), sg.Button('Cancel')]]

    window = sg.Window('File Decryption', layout)

    
    # Proceed with decryption
    with open("filekey.key", "rb") as f:  # Read the key
        key = f.read()

    cipher = Fernet(key)

    # Read the encrypted data
    with open(encrypted_file_path, 'rb') as file:
        all_data = file.readlines()
        encrypted_img = all_data[0]
        encrypted_data = all_data[1]

    dec_path = img_attempt_path.rsplit('.png', 1)[0]+'dec.png'
    try:
        decrypted_data = cipher.decrypt(encrypted_data)
        decode_png(encrypted_img, dec_path)
    except Exception as e:
        sg.popup(f"Decryption failed: {e}")
        return
    
    valid_user = faceFromPath(img_attempt_path, dec_path)
    if valid_user:
        # Get the original file path (without .encrypted extension)
        file_path = encrypted_file_path.rsplit('.encrypted', 1)[0]
        # Write the decrypted data back to the original file
        with open(file_path, 'wb') as file:
            file.write(decrypted_data)
        # Remove the encrypted file
        os.remove(encrypted_file_path)
        sg.popup('File successfully decrypted.')
    else:
        sg.popup('Facial authentification failed.')
        

# Example usage with a simple GUI for file path input
def main(setup: bool):
    if setup: sg.theme('Default1')
    
    layout = [
        [sg.Frame('', layout=[
            [sg.Text('Take an image of yourself:'), 
             sg.Button('Show webcam', key='t_cam')]
        ])],
        [sg.Image(filename='', key='webcam')],
        [sg.Button('Take Image', key='img', disabled=True), 
         sg.Button('Reset', key='reset', disabled=True)],
        [sg.Text('Select a file to encrypt:')],
        [sg.InputText(key='file_path'), sg.FileBrowse()],
        [sg.Button('Encrypt File', key='enc', expand_x=True), 
         sg.Button('Decrypt File', key='dec', expand_x=True)],
        [sg.Text('')],
        [sg.Frame('', layout=[
            [sg.Combo(sg.theme_list(), key='dd', readonly=True, enable_events=True),
            sg.Button('Set Theme', key='st', )]
        ])]
    ]

    window = sg.Window('FaceCript.ai', layout)
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
        
        if event == 'st':
            selected = values['dd']
            if selected:
                sg.theme(selected)
                vid.release()
                window.close()
                main(0)
        
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
                exe_path = encrypt_file(file_path, cam_img)
                sg.popup(f'File encrypted and saved as {exe_path}')
        elif event == 'dec':
            file_path = values['file_path']
            if file_path:
                decrypt_file(file_path, cam_img)

    vid.release()
    window.close()


if __name__ == '__main__':
    main(1)
