# Steganography

A Python desktop application that demonstrates two classic image steganography techniques using **OpenCV** and **PyQt5**. It was developed as an educational/academic project exploring how information can be concealed inside image files, and lets users hide and recover a "message" image inside a "carrier" image using two different embedding approaches.

## Features

- Drag-and-drop or file-browser upload for carrier and message images
- Two selectable hiding (encode) methods: **LSB** and **EOF**
- Two matching extraction (decode) methods for each technique
- Live in-app preview of the resulting stego image or recovered file
- One-click "Download Result" to save the output
- Encrypt/Decrypt mode toggle that switches the visible controls accordingly

## Steganography Methods

### LSB image embedding
The carrier image's low 4 bits (per color channel) are cleared and replaced with the high 4 bits of the message image, which is first resized to match the carrier's dimensions. The original message dimensions are stored in the first two pixels so the image can be resized back on extraction. This method is lossy — the recovered image is a lower-fidelity, "posterized" version of the original.

### EOF file embedding
The message file's raw bytes are appended to the end of the carrier image file, separated by a marker string. On extraction, the marker is located and everything after it is written back out as the recovered file. This method is byte-for-byte lossless, but it does not survive re-compression or re-saving of the image, and its presence can be detected by scanning the file for the marker or comparing file size.

> **Note:** Both methods are **steganography, not encryption**. They conceal data rather than protect it — anyone with the file (and, for EOF, even a text search) can recover the hidden content. No password or cryptographic protection is applied.

## Screenshots

| | |
|---|---|
| ![Main application window](app_photos/Screenshot%202026-07-24%20165340.png) | **Main window.** Encrypt mode, ready for input — drag & drop or browse to select a carrier and message image. |
| ![Hiding a message with the LSB method](app_photos/Screenshot%202026-07-24%20165415.png) | **Hiding data (LSB method).** After choosing a carrier and message image and clicking *Hide (LSB)*, the resulting stego image is shown in the preview pane. The same workflow applies to *Hide (EOF)*. |
| ![Recovering a hidden image with the LSB method](app_photos/Screenshot%202026-07-24%20165448.png) | **Recovering data (LSB method).** In Decrypt mode, clicking *Expose (LSB)* extracts and previews the hidden image from the stego file. The same workflow applies to *Expose (EOF)*. |

## Technologies

- Python
- PyQt5
- OpenCV
- NumPy

## Installation

```bash
pip install opencv-python numpy PyQt5
cd pythonProject
python app.py
```

Alternatively, install from `requirements.txt`:

```bash
pip install -r requirements.txt
cd pythonProject
python app.py
```

## Usage

1. Choose **Encrypt** (to hide data) or **Decrypt** (to recover data).
2. Upload the **Carrier Image** — the image that will hold the hidden data.
3. In Encrypt mode, also upload the **Message Image** — the image to hide.
4. Choose a method: **LSB** or **EOF**, for hiding (*Hide*) or recovering (*Expose*).
5. Preview the resulting image in the app.
6. Click **Download Result** to save the output to disk.

## Project Structure

```
Steganography-main/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── app_photos/                                        # Application screenshots used in this README
├── pythonProject/
│   ├── app.py                                          # PyQt5 GUI entry point
│   ├── LSB_encode.py / LSB_decode.py                   # LSB hide / extract logic
│   ├── EOF_encode.py / EOF_decode.py                   # EOF hide / extract logic
│   └── chameleon.jpg, tiger.jpg                        # Sample images for testing
├── Стеганографија на слики со OpenCV и Python.pdf      # Theory behind the project
└── Стеганографија.pptx                                 # Presentation slides on the same topic
```

The accompanying PDF and PowerPoint presentation explain the theory behind image steganography and the two techniques implemented here.

## Limitations

- The LSB method is lossy — the recovered image loses color resolution and detail.
- The EOF method's hidden data can be detected via marker/file-size inspection and is destroyed by re-compressing or re-saving the stego image.
- No encryption or password protection is implemented; this project demonstrates concealment, not cryptographic security.

## License

This project is licensed under the [MIT License](LICENSE).
