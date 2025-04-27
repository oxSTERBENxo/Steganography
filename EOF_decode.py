import cv2
import os

def decode(stego_path, recovered_secret_path):
    with open(stego_path, 'rb') as f:
        data = f.read()

    marker = b'STEGANOMARKER'
    marker_index = data.find(marker)

    if marker_index == -1:
        return

    secret_data = data[marker_index + len(marker):]

    with open(recovered_secret_path, 'wb') as f:
        f.write(secret_data)
