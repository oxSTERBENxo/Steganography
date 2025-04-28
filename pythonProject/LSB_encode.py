import cv2
import numpy as np

def encode_image(cover_path, secret_path, output_path):

    cover = cv2.imread(cover_path)
    secret = cv2.imread(secret_path)

    orig_h, orig_w = secret.shape[:2]

    secret = cv2.resize(secret, (cover.shape[1], cover.shape[0]), interpolation=cv2.INTER_LANCZOS4)

    cover_cleared = cv2.bitwise_and(cover, np.full(cover.shape, 240, dtype=np.uint8))

    secret_shrunk = secret >> 4

    stego = cv2.bitwise_or(cover_cleared, secret_shrunk)

    stego[0, 0, 0] = (orig_w >> 8) & 0xFF
    stego[0, 0, 1] = orig_w & 0xFF
    stego[0, 1, 0] = (orig_h >> 8) & 0xFF
    stego[0, 1, 1] = orig_h & 0xFF

    cv2.imwrite(output_path, stego)


