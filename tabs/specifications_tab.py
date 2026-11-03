from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
    QHBoxLayout, QMessageBox, QCheckBox, QDialog, QSizePolicy, QSpacerItem
)
from models import Specification
from dialogs.specification_dialog import SpecificationDialog


class SpecificationsTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # --- Кнопки ---
        self.button_layout = QHBoxLayout()
        self.button_layout.setContentsMargins(0, 20, 0, 20)  # відступи: ліво, верх, право, низ
        self.button_layout.setSpacing(20)  # відстань між кнопками

        self.add_btn = QPushButton("Додати")
        self.edit_btn = QPushButton("Редагувати")
        self.delete_btn = QPushButton("Видалити")

        self.button_layout.addWidget(self.add_btn)
        self.button_layout.addWidget(self.edit_btn)
        self.button_layout.addWidget(self.delete_btn)

        # Spacer для вирівнювання зліва
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.button_layout.addItem(spacer)

        self.layout.addLayout(self.button_layout)


        # --- Таблиця ---
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Пристрій", "Роздільна здатність", "Шв. друку", "Шв. сканування",
            "Колір", "Інтерфейс", "Розмір паперу", "Двосторонній"
        ])

        # Виділяти весь рядок
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        # Дозволити виділення лише одного рядка одночасно
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        self.table.setColumnWidth(0, 240)
        self.table.setColumnWidth(1, 180)    
        self.table.setColumnWidth(2, 110)    
        self.table.setColumnWidth(3, 140)
        self.table.setColumnWidth(4, 110)
        self.table.setColumnWidth(5, 180)
        self.table.setColumnWidth(6, 150)
        self.table.setColumnWidth(7, 130)
        

        self.layout.addWidget(self.table)

        # --- Події ---
        self.add_btn.clicked.connect(self.add_spec)
        self.edit_btn.clicked.connect(self.edit_spec)
        self.delete_btn.clicked.connect(self.delete_spec)

        # --- Завантаження ---
        self.load_data()

    def load_data(self):
        """Завантаження даних у таблицю."""
        self.table.setRowCount(0)
        specs = self.db.get_specifications()
        devices = {d.id: d.name for d in self.db.get_devices()}
        types = {d.id: d.device_type_id for d in self.db.get_devices()}

        for spec in specs:
            row = self.table.rowCount()
            self.table.insertRow(row)

            device_name = devices.get(spec.device_id, "Невідомо")
            device_type = types.get(spec.device_id, None)

            # Якщо пристрій не МФУ — швидкість сканування не показуємо
            scan_speed = spec.scan_speed if (device_type == 3 and spec.scan_speed) else "–"

            self.table.setItem(row, 0, QTableWidgetItem(device_name))
            self.table.setItem(row, 1, QTableWidgetItem(spec.resolution or ""))
            self.table.setItem(row, 2, QTableWidgetItem(spec.print_speed or ""))
            self.table.setItem(row, 3, QTableWidgetItem(scan_speed or "–"))
            self.table.setItem(row, 4, QTableWidgetItem(spec.color or ""))
            self.table.setItem(row, 5, QTableWidgetItem(spec.interface or ""))
            self.table.setItem(row, 6, QTableWidgetItem(spec.paper_size or ""))
            self.table.setItem(row, 7, QTableWidgetItem("✅" if spec.duplex else "❌"))

    def add_spec(self):
        dialog = SpecificationDialog(self.db)
        if dialog.exec_() == QDialog.Accepted:
            spec = dialog.get_specification()
            self.db.add_specification(spec)
            self.load_data()

    def edit_spec(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Помилка", "Оберіть рядок для редагування")
            return

        spec = self.db.get_specifications()[row]
        dialog = SpecificationDialog(self.db, spec)
        if dialog.exec_() == QDialog.Accepted:
            updated_spec = dialog.get_specification()
            updated_spec.id = spec.id
            self.db.update_specification(updated_spec)
            self.load_data()

    def delete_spec(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Помилка", "Оберіть рядок для видалення")
            return

        spec = self.db.get_specifications()[row]
        confirm = QMessageBox.question(
            self, "Підтвердити",
            f"Видалити характеристику для пристрою '{spec.device_id}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.db.delete_specification(spec.id)
            self.load_data()