import cv2

def decode_image(stego_path, output_path):
    stego = cv2.imread(stego_path)

    if stego is None:
        return

    extracted_bits = stego & 0b00001111
    secret = extracted_bits << 4

    cv2.imwrite(output_path, secret)
