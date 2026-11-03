# tabs/images_tab.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout,
    QMessageBox, QDialog
)
from models import Image
from dialogs.image_dialog import ImageDialog  # діалогове вікно для додавання/редагування

class ImagesTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # --- Кнопки CRUD над таблицею ---
        # --- 🔘 Кнопки ---
        self.button_layout = QHBoxLayout()
        self.button_layout.setContentsMargins(0, 20, 0, 20)  # відступи: ліво, верх, право, низ
        self.button_layout.setSpacing(20)  # відстань між кнопками

        self.add_btn = QPushButton("Додати")
        self.add_btn.setFixedWidth(140)
        self.edit_btn = QPushButton("Редагувати")
        self.edit_btn.setFixedWidth(140)
        self.delete_btn = QPushButton("Видалити")
        self.delete_btn.setFixedWidth(140)

        self.button_layout.addWidget(self.add_btn)
        self.button_layout.addWidget(self.edit_btn)
        self.button_layout.addWidget(self.delete_btn)
        self.button_layout.addStretch()  # зайвий простір справа, щоб вирівняти кнопки ліворуч

        self.layout.addLayout(self.button_layout)

        # --- Таблиця ---
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Пристрій", "Шлях до файлу", "Опис"])

        # Виділяти весь рядок
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        # Дозволити виділення лише одного рядка одночасно
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setColumnHidden(0, True)
        self.table.setColumnWidth(1, 250)    
        self.table.setColumnWidth(2, 220)    
        self.table.setColumnWidth(3, 260)

        self.layout.addWidget(self.table)

        # --- Події ---
        self.add_btn.clicked.connect(self.add_image)
        self.edit_btn.clicked.connect(self.edit_image)
        self.delete_btn.clicked.connect(self.delete_image)

        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        images = self.db.get_images()
        devices = {d.id: d.name for d in self.db.get_devices()}

        for img in images:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(img.id)))
            self.table.setItem(row, 1, QTableWidgetItem(devices.get(img.device_id, "Невідомо")))
            self.table.setItem(row, 2, QTableWidgetItem(img.file_path or ""))
            self.table.setItem(row, 3, QTableWidgetItem(img.description or ""))

    def add_image(self):
        dialog = ImageDialog(self.db)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            img = Image(**data)
            self.db.add_image(img)
            self.load_data()

    def edit_image(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Помилка", "Оберіть рядок для редагування")
            return
        img_id = int(self.table.item(row, 0).text())
        img = next((i for i in self.db.get_images() if i.id == img_id), None)
        if not img:
            return

        dialog = ImageDialog(self.db, img)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            img.device_id = data["device_id"]
            img.file_path = data["file_path"]
            img.description = data["description"]
            self.db.update_image(img)
            self.load_data()

    def delete_image(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Помилка", "Оберіть рядок для видалення")
            return
        img_id = int(self.table.item(row, 0).text())
        confirm = QMessageBox.question(
            self, "Підтвердити", f"Видалити зображення ID {img_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.db.delete_image(img_id)
            self.load_data()
