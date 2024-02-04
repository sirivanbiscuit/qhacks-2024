import base64
import os
def encode_png(file_path):
    try:
        with open(file_path, "rb") as file:
            file_content = file.read()

        encoded_content = base64.b64encode(file_content).decode("utf-8")

        # Print the encoded content for debugging
        print(f"Encoded Content: {encoded_content}")

        # Write the encoded content to a new file called encoded_photos.txt
        with open("encoded_photos.txt", "w") as photos_file:
            photos_file.write(encoded_content)
        os.remove(file_path)
        return encoded_content
    except Exception as e:
        print(f"Error encoding file: {e}")
        return None

def decode_png(encoded_content, output_file_path):
    try:
        decoded_content = base64.b64decode(encoded_content)

        # Write the decoded content to the specified output file path
        with open(output_file_path, "wb") as f:
            f.write(decoded_content)

        print(f"Decoded content written to {output_file_path}")
    except Exception as e:
        print(f"Error decoding content: {e}")

# Example usage with a PNG file
file_path = r"C:\Users\UCA\Downloads\WIN_20240203_18_20_35_Pro.png"


# Replace with the actual file path
encoded = encode_png(file_path)
input(f"encoded:")
decode_png(encoded, file_path)
