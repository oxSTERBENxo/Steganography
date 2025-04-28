import sys
import os
import shutil
import tempfile
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QFrame
)
from PyQt5.QtGui import QPixmap, QFont, QDragEnterEvent, QDropEvent
from PyQt5.QtCore import Qt

from LSB_encode import encode_image as lsb_encode
from LSB_decode import decode_image as lsb_decode
from EOF_encode import encode as eof_encode
from EOF_decode import decode as eof_decode

ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png')

def is_image(file_path):
    return file_path.lower().endswith(ALLOWED_EXTENSIONS)

class UploadBox(QFrame):
    def __init__(self, parent, title_text):
        super().__init__(parent)
        self.file_path = None
        self.enabled = True
        self.parent_widget = parent
        self.setAcceptDrops(True)
        self.setObjectName('uploadBox')

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        self.title = QLabel(title_text)
        self.title.setFont(QFont('Arial', 11))
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        self.icon = QLabel("📁")
        self.icon.setFont(QFont('Arial', 50))
        self.icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.icon)

        self.instruction = QLabel("Drag & Drop or Browse")
        self.instruction.setFont(QFont('Arial', 14))
        self.instruction.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.instruction)

        self.support = QLabel("Supports: JPG, PNG")
        self.support.setFont(QFont('Arial', 10))
        self.support.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.support)

        self.setFixedSize(400, 300)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if self.enabled and event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if self.enabled and event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            if is_image(file_path):
                self.set_file(file_path)

    def mousePressEvent(self, event):
        if self.enabled:
            path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
            if path:
                self.set_file(path)

    def set_file(self, path):
        if not is_image(path):
            return
        self.file_path = path
        pixmap = QPixmap(path).scaled(self.width() - 20, self.height() - 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon.setPixmap(pixmap)

        self.instruction.setText("Drag & Drop or Browse")
        self.support.setText("Supports: JPG, PNG")

        if self.parent_widget:
            self.parent_widget.update_action_btn()

    def clear(self):
        self.file_path = None
        self.icon.setPixmap(QPixmap())
        self.icon.setText("📁")
        self.instruction.setText("Drag & Drop or Browse")
        self.support.setText("Supports: JPG, PNG")

    def set_enabled(self, enabled):
        self.enabled = enabled
        if not enabled:
            self.setStyleSheet("background-color: #eeeeee; border: 2px dashed #ccc; border-radius: 15px;")
        else:
            self.setStyleSheet("")


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Encrypt/Decrypt Uploader")
        self.setGeometry(300, 50, 1200, 1100)

        self.mode = 'Encrypt'
        self.temp_result = None
        self.temp_files = []

        self.init_ui()

    def init_ui(self):
        self.container = QFrame(self)
        self.container.setObjectName('container')
        self.container.setGeometry(30, 20, 1140, 1040)

        self.main_layout = QVBoxLayout(self.container)
        self.main_layout.setAlignment(Qt.AlignTop)
        self.main_layout.setSpacing(20)

        self.encrypt_btn = QPushButton('🔒 Encrypt')
        self.decrypt_btn = QPushButton('🔓 Decrypt')
        self.encrypt_btn.clicked.connect(self.switch_encrypt)
        self.decrypt_btn.clicked.connect(self.switch_decrypt)

        toggle_layout = QHBoxLayout()
        toggle_layout.addWidget(self.encrypt_btn)
        toggle_layout.addWidget(self.decrypt_btn)

        self.carrier_box = UploadBox(self, 'Carrier Image')
        self.message_box = UploadBox(self, 'Message Image')

        upload_layout = QHBoxLayout()
        upload_layout.addStretch()
        upload_layout.addWidget(self.carrier_box)
        upload_layout.addSpacing(40)
        upload_layout.addWidget(self.message_box)
        upload_layout.addStretch()

        self.hide_lsb_btn = QPushButton('Hide (LSB)')
        self.hide_eof_btn = QPushButton('Hide (EOF)')
        self.expose_lsb_btn = QPushButton('Expose (LSB)')
        self.expose_eof_btn = QPushButton('Expose (EOF)')

        self.hide_lsb_btn.clicked.connect(self.hide_lsb)
        self.hide_eof_btn.clicked.connect(self.hide_eof)
        self.expose_lsb_btn.clicked.connect(self.expose_lsb)
        self.expose_eof_btn.clicked.connect(self.expose_eof)

        self.result_image = QLabel("")
        self.result_image.setFixedSize(500, 350)
        self.result_image.setAlignment(Qt.AlignCenter)

        self.download_result_btn = QPushButton("Download Result")
        self.download_result_btn.setEnabled(False)
        self.download_result_btn.clicked.connect(self.download_result)

        self.main_layout.addLayout(toggle_layout)
        self.main_layout.addLayout(upload_layout)
        self.main_layout.addWidget(self.hide_lsb_btn)
        self.main_layout.addWidget(self.hide_eof_btn)
        self.main_layout.addWidget(self.expose_lsb_btn)
        self.main_layout.addWidget(self.expose_eof_btn)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.result_image, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.download_result_btn)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
            }
            #container {
                background-color: white;
                border-radius: 20px;
                padding: 30px;
            }
            QPushButton {
                height: 50px;
                font-size: 16px;
                border-radius: 10px;
            }
            QPushButton:enabled {
                background-color: #4a69bd;
                color: white;
            }
            QPushButton:disabled {
                background-color: lightgray;
                color: gray;
            }
            #uploadBox {
                border: 2px dashed #ccc;
                background-color: #fafafa;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        self.update_mode_view()

    def switch_encrypt(self):
        self.mode = 'Encrypt'
        self.reset_app()

    def switch_decrypt(self):
        self.mode = 'Decrypt'
        self.reset_app()

    def reset_app(self):
        self.carrier_box.clear()
        self.message_box.clear()
        self.temp_result = None
        self.result_image.clear()
        self.download_result_btn.setEnabled(False)
        self.update_mode_view()

    def update_mode_view(self):
        if self.mode == "Encrypt":
            self.message_box.show()
            self.hide_lsb_btn.show()
            self.hide_eof_btn.show()
            self.expose_lsb_btn.hide()
            self.expose_eof_btn.hide()
        else:
            self.message_box.hide()
            self.hide_lsb_btn.hide()
            self.hide_eof_btn.hide()
            self.expose_lsb_btn.show()
            self.expose_eof_btn.show()

        self.encrypt_btn.setText("🔒 Encrypt")
        self.decrypt_btn.setText("🔓 Decrypt")
        for button in [self.hide_lsb_btn, self.hide_eof_btn, self.expose_lsb_btn, self.expose_eof_btn]:
            button.setStyleSheet("background-color: lightgray; color: gray; border-radius: 10px;")

        if self.mode == "Encrypt":
            self.encrypt_btn.setStyleSheet("background-color: #4a69bd; color: white; border-radius: 10px;")
            self.decrypt_btn.setStyleSheet("background-color: lightgray; color: gray; border-radius: 10px;")
        else:
            self.decrypt_btn.setStyleSheet("background-color: #4a69bd; color: white; border-radius: 10px;")
            self.encrypt_btn.setStyleSheet("background-color: lightgray; color: gray; border-radius: 10px;")

        self.update_action_btn()

    def create_temp_file(self):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        self.temp_files.append(temp_file.name)
        temp_file.close()
        return temp_file.name

    def hide_lsb(self):
        temp_path = self.create_temp_file()
        lsb_encode(self.carrier_box.file_path, self.message_box.file_path, temp_path)
        self.show_result(temp_path)
        self.encrypt_btn.setText("🗑️ Clear")
        self.hide_lsb_btn.setStyleSheet("background-color: #4a69bd; color: white; border-radius: 10px;")
        self.hide_eof_btn.setStyleSheet("background-color: lightgray; color: gray; border-radius: 10px;")

    def hide_eof(self):
        temp_path = self.create_temp_file()
        eof_encode(self.carrier_box.file_path, self.message_box.file_path, temp_path)
        self.show_result(temp_path)
        self.encrypt_btn.setText("🗑️ Clear")
        self.hide_eof_btn.setStyleSheet("background-color: #4a69bd; color: white; border-radius: 10px;")
        self.hide_lsb_btn.setStyleSheet("background-color: lightgray; color: gray; border-radius: 10px;")

    def expose_lsb(self):
        temp_path = self.create_temp_file()
        lsb_decode(self.carrier_box.file_path, temp_path)
        self.show_result(temp_path)
        self.decrypt_btn.setText("🗑️ Clear")
        self.expose_lsb_btn.setStyleSheet("background-color: #4a69bd; color: white; border-radius: 10px;")
        self.expose_eof_btn.setStyleSheet("background-color: lightgray; color: gray; border-radius: 10px;")

    def expose_eof(self):
        temp_path = self.create_temp_file()
        eof_decode(self.carrier_box.file_path, temp_path)
        self.show_result(temp_path)
        self.decrypt_btn.setText("🗑️ Clear")
        self.expose_eof_btn.setStyleSheet("background-color: #4a69bd; color: white; border-radius: 10px;")
        self.expose_lsb_btn.setStyleSheet("background-color: lightgray; color: gray; border-radius: 10px;")

    def show_result(self, path):
        self.temp_result = path
        pixmap = QPixmap(path)
        pixmap = pixmap.scaled(self.result_image.width(), self.result_image.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.result_image.setPixmap(pixmap)
        self.download_result_btn.setEnabled(True)

    def download_result(self):
        if self.temp_result:
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Result", os.path.basename(self.temp_result), "Image Files (*.png *.jpg)")
            if save_path:
                shutil.copy(self.temp_result, save_path)

    def update_action_btn(self):
        ready_encrypt = self.carrier_box.file_path and self.message_box.file_path
        ready_decrypt = self.carrier_box.file_path

        if self.mode == "Encrypt":
            self.hide_lsb_btn.setEnabled(bool(ready_encrypt))
            self.hide_eof_btn.setEnabled(bool(ready_encrypt))
        else:
            self.expose_lsb_btn.setEnabled(bool(ready_decrypt))
            self.expose_eof_btn.setEnabled(bool(ready_decrypt))

    def closeEvent(self, event):
        for file_path in self.temp_files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error deleting temp file {file_path}: {e}")
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
