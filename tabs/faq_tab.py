from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout,
    QMessageBox, QDialog
)
from models import FAQ
from dialogs.faq_dialog import FAQDialog  # окремий діалог для FAQ

class FAQTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # --- Кнопки CRUD над таблицею ---

        self.button_layout = QHBoxLayout()
        self.button_layout.setContentsMargins(0, 20, 0, 20)  # ліво, верх, право, низ
        self.button_layout.setSpacing(20)  # відстань між кнопками

        self.add_btn = QPushButton("Додати")
        self.add_btn.setFixedWidth(140)
        self.edit_btn = QPushButton("Редагувати")
        self.edit_btn.setFixedWidth(140)
        self.delete_btn = QPushButton("Видалити")
        self.delete_btn.setFixedWidth(140)

        # додаємо кнопки та вирівнюємо їх ліворуч
        self.button_layout.addWidget(self.add_btn)
        self.button_layout.addWidget(self.edit_btn)
        self.button_layout.addWidget(self.delete_btn)
        self.button_layout.addStretch()  # щоб зайвий простір залишився справа

        self.layout.addLayout(self.button_layout)

        # --- Таблиця ---
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Пристрій", "Питання", "Відповідь"])
        # Виділяти весь рядок
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        # Дозволити виділення лише одного рядка одночасно
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setColumnHidden(0, True)
        self.table.setColumnWidth(1, 230)    
        self.table.setColumnWidth(2, 280)    
        self.table.setColumnWidth(3, 500)

        self.layout.addWidget(self.table)

        # --- Події ---
        self.add_btn.clicked.connect(self.add_faq)
        self.edit_btn.clicked.connect(self.edit_faq)
        self.delete_btn.clicked.connect(self.delete_faq)

        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        faqs = self.db.get_faqs()
        devices = {d.id: d.name for d in self.db.get_devices()}

        for f in faqs:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(f.id)))
            device_name = devices.get(f.device_id, "Загальне") if f.device_id else "Загальне"
            self.table.setItem(row, 1, QTableWidgetItem(device_name))
            self.table.setItem(row, 2, QTableWidgetItem(f.question or ""))
            self.table.setItem(row, 3, QTableWidgetItem(f.answer or ""))

    def add_faq(self):
        dialog = FAQDialog(self.db)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            faq = FAQ(**data)
            self.db.add_faq(faq)
            self.load_data()

    def edit_faq(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Помилка", "Оберіть рядок для редагування")
            return
        faq_id = int(self.table.item(row, 0).text())
        faq = next((f for f in self.db.get_faqs() if f.id == faq_id), None)
        if not faq:
            return

        dialog = FAQDialog(self.db, faq)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            faq.device_id = data["device_id"]
            faq.question = data["question"]
            faq.answer = data["answer"]
            self.db.update_faq(faq)
            self.load_data()

    def delete_faq(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Помилка", "Оберіть рядок для видалення")
            return
        faq_id = int(self.table.item(row, 0).text())
        confirm = QMessageBox.question(
            self, "Підтвердити", f"Видалити FAQ ID {faq_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.db.delete_faq(faq_id)
            self.load_data()
