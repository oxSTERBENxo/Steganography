import cv2
import numpy as np

def decode_image(stego_path, output_path):

    stego = cv2.imread(stego_path)

    high_w = int(stego[0, 0, 0]); low_w = int(stego[0, 0, 1])
    high_h = int(stego[0, 1, 0]); low_h = int(stego[0, 1, 1])
    orig_w = (high_w << 8) | low_w
    orig_h = (high_h << 8) | low_h

    extracted_bits = cv2.bitwise_and(stego, np.full(stego.shape, 15, dtype=np.uint8))

    secret = extracted_bits << 4

    recovered = cv2.resize(secret, (orig_w, orig_h), interpolation=cv2.INTER_LANCZOS4)

    cv2.imwrite(output_path, recovered)
