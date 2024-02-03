import os
import os.path
import shutil
from cryptography.fernet import Fernet
import getpass

# A complete working version of the program without the facial recognition software.
# This program will be an exe that sucks a selected file into itself, and spits it out
# once the user gives the correct passcode.

def validate_file_existence(file_path):
    """ Validates the existence of the selected file.
    @:param: file_path - path to selected file
    @:return: True if file exists
    @:return: False if file does not exist"""

    if os.path.isfile(file_path):
        print("We're in!")
        return True
    else:
        print("File not found.")
        return False

def encrypt_passcode(passcode):
    """ Applies encryption or hashing to the user's passcode.
     @:param: passcode - user provided passcode
     @:return: encrypted or hashed version of the passcode."""
    print (f'You entered: {passcode}')
    print("encoding...")

    # key generation
    key = Fernet.generate_key()
    # string the key in a file
    with open("filekey.key", "wb") as filekey:
        filekey.write(key)
        print(key)




def lock_file(file_path, encrypted_passcode):
    """Locks the selected file using the provided passcode.
    @:param: file_path - Path to the selected file.
    @:param: encrypted_passcode - Encrypted or hashed passcode."""

    # opening the key
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()

    # using the generated key
    fernet = Fernet(key)

    # opening the original file to encrypt
    with open(file_path, 'rb') as file:
        original = file.read()

    # encrypting the file
    encrypted = fernet.encrypt(original)

    # opening the file in write mode and
    # writing the encrypted data
    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def unlock_file(file_path, encrypted_passcode):
    """Unlocks the file if the provided passcode matches.
    @:param: file_path - Path to the locked file.
    @:param: encrypted_passcode - Encrypted or hashed passcode."""
    # # copy tree
    # shutil.copytree("C:/Users/Mark/Desktop/a", "C:/Users/Mark/Desktop/b/a")
    # # remove tree
    # shutil.rmtree("C:/Users/Mark/Desktop/b/a")
    # # move text file into tree
    # shutil.copy("C:/Users/Mark/Desktop/a/failed careers.txt", "C:/Users/Mark/Desktop/b")

def main():
    #Display user-friendly menu w/. options to lock/unlock the file or exit
    #Call corresponding functions
    print("Hi buddy...")
    file_path = input("What file are we peeping into?")

    #TODO: change/delete path_path input as rn the input is null
    FILE_PATH = "C:/Users/Mark/Desktop/failed careers.txt"

    if validate_file_existence(FILE_PATH):
        passcode = input("What... is your favourite colour? ")

        # Use getpass to securely input the passcode from the user. BUT IT DOESN'T WORK
        # TODO: Decide on a simple encryption or hashing method to store and verify the passcode.
        # Implement functions to lock and unlock the file using the passcode.

        encrypt_passcode(passcode)
        unlock_file(FILE_PATH, passcode)

    else:
        print ("meh")



if __name__ == "__main__":
    main()
