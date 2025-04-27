import cv2

def encode_image(cover_path, secret_path, output_path):
    cover = cv2.imread(cover_path)
    secret = cv2.imread(secret_path)

    if cover is None or secret is None:
        return

    secret = cv2.resize(secret, (cover.shape[1], cover.shape[0]))

    cover_cleared = cover & 0b11110000
    secret_shrunk = secret >> 4
    stego = cover_cleared | secret_shrunk

    cv2.imwrite(output_path, stego)

