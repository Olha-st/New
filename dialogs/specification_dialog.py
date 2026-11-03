from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, 
    QHBoxLayout, QMessageBox, QCheckBox, QHeaderView, QDialog, QFormLayout,
)

from PyQt5.QtWidgets import QComboBox, QLineEdit, QDialogButtonBox, QGridLayout
from models import Specification

class SpecificationDialog(QDialog):
    def __init__(self, db, spec=None):
        super().__init__()
        self.db = db
        self.spec = spec
        self.setWindowTitle("Характеристики пристрою")
        self.setMinimumWidth(400)

        layout = QFormLayout(self)

        # Пристрій
        self.device_cb = QComboBox()
        self.devices = db.get_devices()
        for d in self.devices:
            self.device_cb.addItem(d.name, d.id)
        layout.addRow("Пристрій:", self.device_cb)

        # Роздільна здатність
        self.resolution_edit = QLineEdit()
        layout.addRow("Роздільна здатність:", self.resolution_edit)

        # Швидкість друку
        self.print_speed_edit = QLineEdit()
        layout.addRow("Швидкість друку:", self.print_speed_edit)

        # Швидкість сканування
        self.scan_speed_edit = QLineEdit()
        layout.addRow("Швидкість сканування:", self.scan_speed_edit)

        # Колір (чекбокси)
        self.color_layout = QHBoxLayout()
        self.color_cb1 = QCheckBox("Кольоровий")
        self.color_cb2 = QCheckBox("Чорно-білий")
        self.color_layout.addWidget(self.color_cb1)
        self.color_layout.addWidget(self.color_cb2)
        layout.addRow("Колір:", self.color_layout)

        # Інтерфейс
        self.interface_layout = QGridLayout()
        self.interface_usb = QCheckBox("USB")
        self.interface_wifi = QCheckBox("Wi-Fi")
        self.interface_eth = QCheckBox("Ethernet")
        self.interface_bt = QCheckBox("Bluetooth")
        self.interface_layout.addWidget(self.interface_usb, 0, 0)
        self.interface_layout.addWidget(self.interface_wifi, 0, 1)
        self.interface_layout.addWidget(self.interface_eth, 1, 0)
        self.interface_layout.addWidget(self.interface_bt, 1, 1)
        layout.addRow("Інтерфейс:", self.interface_layout)

        # Розмір паперу
        self.paper_layout = QHBoxLayout()
        self.paper_a4 = QCheckBox("A4")
        self.paper_a5 = QCheckBox("A5")
        self.paper_a3 = QCheckBox("A3")
        self.paper_layout.addWidget(self.paper_a4)
        self.paper_layout.addWidget(self.paper_a5)
        self.paper_layout.addWidget(self.paper_a3)
        layout.addRow("Розмір паперу:", self.paper_layout)

        # Двосторонній друк
        self.duplex_cb = QCheckBox("Двосторонній друк")
        layout.addRow("", self.duplex_cb)

        # Кнопки
        self.buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        if spec:
            self.load_spec(spec)

    def load_spec(self, spec):
        self.device_cb.setCurrentIndex(next(
            (i for i, d in enumerate(self.devices) if d.id == spec.device_id), 0
        ))
        self.resolution_edit.setText(spec.resolution or "")
        self.print_speed_edit.setText(spec.print_speed or "")
        self.scan_speed_edit.setText(spec.scan_speed or "")

        # Колір
        if spec.color:
            colors = [c.strip().lower() for c in spec.color.split(",")]
            self.color_cb1.setChecked("кольоровий" in colors)
            self.color_cb2.setChecked("чорно-білий" in colors)

        # Інтерфейс
        if spec.interface:
            interfaces = [i.strip().lower() for i in spec.interface.split(",")]
            self.interface_usb.setChecked("usb" in interfaces)
            self.interface_wifi.setChecked("wi-fi" in interfaces)
            self.interface_eth.setChecked("ethernet" in interfaces)
            self.interface_bt.setChecked("bluetooth" in interfaces)

        # Папір
        if spec.paper_size:
            papers = [p.strip().lower() for p in spec.paper_size.split(",")]
            self.paper_a4.setChecked("a4" in papers)
            self.paper_a5.setChecked("a5" in papers)
            self.paper_a3.setChecked("a3" in papers)

        self.duplex_cb.setChecked(bool(spec.duplex))

    def get_specification(self):
        """Отримати значення з діалогу у вигляді об’єкта Specification."""
        device_id = self.device_cb.currentData()
        color = ", ".join(
            c for cb, c in [
                (self.color_cb1, "Кольоровий"),
                (self.color_cb2, "Чорно-білий"),
            ] if cb.isChecked()
        )
        interface = ", ".join(
            i for cb, i in [
                (self.interface_usb, "USB"),
                (self.interface_wifi, "Wi-Fi"),
                (self.interface_eth, "Ethernet"),
                (self.interface_bt, "Bluetooth"),
            ] if cb.isChecked()
        )
        paper_size = ", ".join(
            p for cb, p in [
                (self.paper_a4, "A4"),
                (self.paper_a5, "A5"),
                (self.paper_a3, "A3"),
            ] if cb.isChecked()
        )

        return Specification(
            device_id=device_id,
            resolution=self.resolution_edit.text(),
            print_speed=self.print_speed_edit.text(),
            scan_speed=self.scan_speed_edit.text(),
            color=color,
            interface=interface,
            paper_size=paper_size,
            duplex=self.duplex_cb.isChecked()
        )