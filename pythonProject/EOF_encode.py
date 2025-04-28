import cv2
import os

def encode(cover_path, secret_path, output_path):
    cover_img = cv2.imread(cover_path)
    if cover_img is None:
        return

    cv2.imwrite(output_path, cover_img)

    with open(output_path, 'ab') as f_out, open(secret_path, 'rb') as f_secret:
        f_out.write(b'STEGANOMARKER')
        f_out.write(f_secret.read())
