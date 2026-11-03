from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QVBoxLayout, QPushButton
from models import Image

class ImageDialog(QDialog):
    def __init__(self, db, image=None):
        super().__init__()
        self.db = db
        self.image = image
        self.setWindowTitle("Зображення")
        self.setFixedWidth(300)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Вибір пристрою
        self.device_combo = QComboBox()
        for d in self.db.get_devices():
            self.device_combo.addItem(d.name, d.id)
        form_layout.addRow("Пристрій:", self.device_combo)

        self.file_path_edit = QLineEdit()
        form_layout.addRow("Шлях до файлу:", self.file_path_edit)

        self.description_edit = QLineEdit()
        form_layout.addRow("Опис:", self.description_edit)

        layout.addLayout(form_layout)

        # Кнопки
        self.save_btn = QPushButton("Зберегти")
        self.cancel_btn = QPushButton("Скасувати")
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        if image:
            self.device_combo.setCurrentIndex(
                self.device_combo.findData(image.device_id)
            )
            self.file_path_edit.setText(image.file_path or "")
            self.description_edit.setText(image.description or "")

    def get_data(self):
        return {
            "device_id": self.device_combo.currentData(),
            "file_path": self.file_path_edit.text(),
            "description": self.description_edit.text()
        }
