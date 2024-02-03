import base64

# Base64-encoded content of the file
embedded_file_content = """
aGVsbG8gbXkgbmFtZSBpcyBtYXJreW1hcms=

"""

# Decode the content
decoded_content = base64.b64decode(embedded_file_content)

    

# Write the decoded content to a file
def decode():
    with open("C:\\Users\\UCA\\Documents\\CISC 121\\output.txt", "wb") as f:
        f.write(decoded_content)
        print("written")

# Now 'output.txt' contains the content of the embedded file
