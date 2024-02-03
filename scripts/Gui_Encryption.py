from cryptography.fernet import Fernet
import PySimpleGUI as sg
import os
import shutil
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
        [sg.Text('Select a file to encrypt:')],
        [sg.InputText(key='file_path'), sg.FileBrowse()],
        [sg.Button('Encrypt to EXE'), sg.Button('Decrypt from EXE')]
    ]

    window = sg.Window('File Encryptor', layout)

    while True:
        event, values = window.read()

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

    window.close()

if __name__ == '__main__':
    main()
