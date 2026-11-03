# dialogs/device_dialog.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QDoubleSpinBox, QPushButton

class DeviceDialog(QDialog):
    def __init__(self, db, device=None):
        super().__init__()
        self.db = db
        self.device = device  # якщо редагування, передається об'єкт Device
        self.setWindowTitle("Пристрій")
        self.setMinimumWidth(400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Назва
        self.name_label = QLabel("Назва:")
        self.name_edit = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_edit)

        # Виробник (ComboBox)
        self.manufacturer_label = QLabel("Виробник:")
        self.manufacturer_combo = QComboBox()
        self.manufacturers = self.db.get_manufacturers()
        for m in self.manufacturers:
            self.manufacturer_combo.addItem(m.name, m.id)
        self.layout.addWidget(self.manufacturer_label)
        self.layout.addWidget(self.manufacturer_combo)

        # Тип пристрою (ComboBox)
        self.type_label = QLabel("Тип пристрою:")
        self.type_combo = QComboBox()
        self.types = self.db.get_device_types()
        for t in self.types:
            self.type_combo.addItem(t.name, t.id)
        self.layout.addWidget(self.type_label)
        self.layout.addWidget(self.type_combo)

        # Ціна
        self.price_label = QLabel("Ціна ($):")
        self.price_spin = QDoubleSpinBox()
        self.price_spin.setRange(0, 100000)
        self.price_spin.setDecimals(2)
        self.layout.addWidget(self.price_label)
        self.layout.addWidget(self.price_spin)

        # Кнопки
        self.button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Зберегти")
        self.cancel_btn = QPushButton("Скасувати")
        self.button_layout.addWidget(self.save_btn)
        self.button_layout.addWidget(self.cancel_btn)
        self.layout.addLayout(self.button_layout)

        # Підключення кнопок
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

        # Якщо редагування, заповнюємо поля
        if self.device:
            self.name_edit.setText(self.device.name)
            index = self.manufacturer_combo.findData(self.device.manufacturer_id)
            if index >= 0:
                self.manufacturer_combo.setCurrentIndex(index)
            index = self.type_combo.findData(self.device.device_type_id)
            if index >= 0:
                self.type_combo.setCurrentIndex(index)
            self.price_spin.setValue(self.device.price)

    def get_data(self):
        return {
            "name": self.name_edit.text(),
            "manufacturer_id": self.manufacturer_combo.currentData(),
            "device_type_id": self.type_combo.currentData(),
            "price": self.price_spin.value()
        }
