from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
    QHBoxLayout, QMessageBox, QDialog, QFormLayout, QLabel,
    QComboBox, QLineEdit, QSpinBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from models import Device
from dialogs.device_dialog import DeviceDialog
import os


from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QFormLayout, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os

class DeviceInfoDialog(QDialog):
    """Діалогове вікно для перегляду характеристик і фото пристрою."""

    def __init__(self, device, spec, manufacturer, device_type, images, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Характеристики пристрою — {device.name}")
        self.setFixedWidth(480)
        self.images = images

        layout = QVBoxLayout()

        # --- 📸 Блок фото ---
        self.photo_label = QLabel()
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setFixedSize(400, 250)

        if self.images:
            self.show_image(0)
        else:
            self.photo_label.setText("Фото відсутні")

        layout.addWidget(self.photo_label)
        layout.addSpacing(10)

        # --- 📋 Основні характеристики ---
        form_layout = QFormLayout()
        form_layout.addRow(QLabel("<b>Назва:</b>"), QLabel(device.name))
        form_layout.addRow(QLabel("<b>Виробник:</b>"), QLabel(manufacturer))
        form_layout.addRow(QLabel("<b>Тип пристрою:</b>"), QLabel(device_type))
        form_layout.addRow(QLabel("<b>Ціна:</b>"), QLabel(f"{device.price} $"))

        # --- 🧩 Технічні характеристики ---
        if spec:
            form_layout.addRow(QLabel("<b>Роздільна здатність:</b>"), QLabel(spec.resolution or "-"))
            form_layout.addRow(QLabel("<b>Швидкість друку:</b>"), QLabel(spec.print_speed or "-"))
            form_layout.addRow(QLabel("<b>Швидкість сканування:</b>"), QLabel(spec.scan_speed or "-"))
            form_layout.addRow(QLabel("<b>Колір:</b>"), QLabel(spec.color or "-"))
            form_layout.addRow(QLabel("<b>Інтерфейси:</b>"), QLabel(spec.interface or "-"))
            form_layout.addRow(QLabel("<b>Розмір паперу:</b>"), QLabel(spec.paper_size or "-"))
            form_layout.addRow(QLabel("<b>Двосторонній друк:</b>"), QLabel("Так" if spec.duplex else "Ні"))
        else:
            form_layout.addRow(QLabel("<b>Характеристики:</b>"), QLabel("Не знайдено"))

        layout.addLayout(form_layout)
        layout.addSpacing(10)

        # --- 🔘 Кнопка закриття ---
        close_btn = QPushButton("Закрити")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)

        self.setLayout(layout)

    def show_image(self, index):
        """Відображає перше фото (якщо є)."""
        if not self.images:
            self.photo_label.setText("Фото відсутні")
            return

        image_path = self.images[index].file_path
        if not os.path.exists(image_path):
            self.photo_label.setText("Фото не знайдено")
            return

        pixmap = QPixmap(image_path).scaled(
            400, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.photo_label.setPixmap(pixmap)



class DevicesTab(QWidget):
    """Вкладка для перегляду, редагування та фільтрації пристроїв."""

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)



        # --- 🔘 Кнопки ---
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 20, 0, 20)  # відступи: ліво, верх, право, низ
        btn_layout.setSpacing(20)  # відстань між кнопками

        self.add_btn = QPushButton("Додати")
        self.edit_btn = QPushButton("Редагувати")
        self.delete_btn = QPushButton("Видалити")

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)

        # Spacer для вирівнювання зліва
        btn_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.layout.addLayout(btn_layout)

        # --- 🔍 Фільтри ---
        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(0, 0, 0, 20)  # відступи зверху/знизу
        filter_layout.setSpacing(20)  # відстань між елементами

        self.type_filter = QComboBox()
        self.type_filter.addItem("Усі типи")
        for t in self.db.get_device_types():
            self.type_filter.addItem(t.name, t.id)

        self.manufacturer_filter = QComboBox()
        self.manufacturer_filter.addItem("Усі виробники")
        for m in self.db.get_manufacturers():
            self.manufacturer_filter.addItem(m.name, m.id)

        self.price_min = QSpinBox()
        self.price_min.setPrefix("Від ")
        self.price_min.setMaximum(10000)
        self.price_min.setValue(0)

        self.price_max = QSpinBox()
        self.price_max.setPrefix("До ")
        self.price_max.setMaximum(10000)
        self.price_max.setValue(10000)

        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("Пошук за назвою...")
        self.search_name.setFixedWidth(140)

        self.reset_btn = QPushButton("Скинути")

        filter_layout.addWidget(QLabel("Тип:"))
        filter_layout.addWidget(self.type_filter)
        filter_layout.addWidget(QLabel("Виробник:"))
        filter_layout.addWidget(self.manufacturer_filter)
        filter_layout.addWidget(self.price_min)
        filter_layout.addWidget(self.price_max)
        filter_layout.addWidget(self.search_name)
        filter_layout.addWidget(self.reset_btn)

        # Spacer для вирівнювання зліва
        filter_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.layout.addLayout(filter_layout)


        # --- 📊 Таблиця ---
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Назва", "Виробник", "Тип пристрою", "Ціна ($)"])
                # Виділяти весь рядок
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        # Дозволити виділення лише одного рядка одночасно
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setColumnHidden(0, True)
        self.table.setColumnWidth(1, 300)    
        self.table.setColumnWidth(2, 170)    
        self.table.setColumnWidth(3, 170)
        self.table.setColumnWidth(4, 160)

        self.layout.addWidget(self.table)
        self.table.itemDoubleClicked.connect(self.show_device_info)


        # Події
        self.add_btn.clicked.connect(self.add_device)
        self.edit_btn.clicked.connect(self.edit_device)
        self.delete_btn.clicked.connect(self.delete_device)
        self.reset_btn.clicked.connect(self.reset_filters)
        self.type_filter.currentIndexChanged.connect(self.load_data)
        self.manufacturer_filter.currentIndexChanged.connect(self.load_data)
        self.price_min.valueChanged.connect(self.load_data)
        self.price_max.valueChanged.connect(self.load_data)
        self.search_name.textChanged.connect(self.load_data)

        self.load_data()

    # --- 📦 Завантаження таблиці ---
    def load_data(self):
        self.table.setRowCount(0)
        devices = self.db.get_devices()
        manufacturers = {m.id: m.name for m in self.db.get_manufacturers()}
        types = {t.id: t.name for t in self.db.get_device_types()}

        selected_type = self.type_filter.currentData()
        selected_manufacturer = self.manufacturer_filter.currentData()
        min_price = self.price_min.value()
        max_price = self.price_max.value()
        search_text = self.search_name.text().lower()

        for d in devices:
            if selected_type and selected_type != d.device_type_id:
                continue
            if selected_manufacturer and selected_manufacturer != d.manufacturer_id:
                continue
            if not (min_price <= d.price <= max_price):
                continue
            if search_text and search_text not in d.name.lower():
                continue

            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(d.id)))
            self.table.setItem(row, 1, QTableWidgetItem(d.name))
            self.table.setItem(row, 2, QTableWidgetItem(manufacturers.get(d.manufacturer_id, "-")))
            self.table.setItem(row, 3, QTableWidgetItem(types.get(d.device_type_id, "-")))
            self.table.setItem(row, 4, QTableWidgetItem(f"{d.price} $"))

    def reset_filters(self):
        self.type_filter.setCurrentIndex(0)
        self.manufacturer_filter.setCurrentIndex(0)
        self.price_min.setValue(0)
        self.price_max.setValue(10000)
        self.search_name.clear()
        self.load_data()

    # --- CRUD ---
    def add_device(self):
        dialog = DeviceDialog(self.db)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            device = Device(**data)
            self.db.add_device(device)
            self.load_data()

    def edit_device(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Помилка", "Оберіть рядок для редагування")
            return
        device_id = int(self.table.item(row, 0).text())
        device = next((d for d in self.db.get_devices() if d.id == device_id), None)
        if not device:
            return
        dialog = DeviceDialog(self.db, device)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            device.name = data["name"]
            device.manufacturer_id = data["manufacturer_id"]
            device.device_type_id = data["device_type_id"]
            device.price = data["price"]
            self.db.update_device(device)
            self.load_data()

    def delete_device(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Помилка", "Оберіть рядок для видалення")
            return
        device_id = int(self.table.item(row, 0).text())
        confirm = QMessageBox.question(self, "Підтвердити", f"Видалити пристрій ID {device_id}?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.db.delete_device(device_id)
            self.load_data()

    # --- 🔍 Подвійний клік ---
    def show_device_info(self, item):
        row = item.row()
        device_id = int(self.table.item(row, 0).text())
        device = next((d for d in self.db.get_devices() if d.id == device_id), None)
        if not device:
            return

        spec = self.db.get_specification_by_device(device_id)
        manufacturer = next((m.name for m in self.db.get_manufacturers() if m.id == device.manufacturer_id), "-")
        device_type = next((t.name for t in self.db.get_device_types() if t.id == device.device_type_id), "-")
        images = self.db.get_images_by_device(device_id)

        dialog = DeviceInfoDialog(device, spec, manufacturer, device_type, images)
        dialog.exec_()
