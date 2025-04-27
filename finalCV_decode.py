import cv2
import numpy as np

def decode_image(stego_path, output_path):
    stego = cv2.imread(stego_path)

    extracted_bits = cv2.bitwise_and(stego, np.full(stego.shape, 15, dtype=np.uint8))

    secret = extracted_bits << 4

    cv2.imwrite(output_path, secret)
