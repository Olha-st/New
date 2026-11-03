from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout,
    QMessageBox, QDialog, QFormLayout, QLineEdit, QSpinBox, QDateEdit
)
from PyQt5.QtCore import QDate
from models import Review
from dialogs.review_dialog import ReviewDialog  # створимо окремий діалог

class ReviewsTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # --- Кнопки CRUD над таблицею ---
        self.button_layout = QHBoxLayout()
        self.button_layout.setContentsMargins(0, 20, 0, 20)  # відступи: ліво, верх, право, низ
        self.button_layout.setSpacing(20)  # відстань між кнопками

        # Створюємо кнопки з фіксованою шириною
        self.add_btn = QPushButton("Додати")
        self.add_btn.setFixedWidth(140)
        self.edit_btn = QPushButton("Редагувати")
        self.edit_btn.setFixedWidth(140)
        self.delete_btn = QPushButton("Видалити")
        self.delete_btn.setFixedWidth(140)

        # Додаємо кнопки до layout та вирівнюємо зліва
        self.button_layout.addWidget(self.add_btn)
        self.button_layout.addWidget(self.edit_btn)
        self.button_layout.addWidget(self.delete_btn)
        self.button_layout.addStretch()  # залишає простір справа

        # Додаємо layout з кнопками у головний layout
        self.layout.addLayout(self.button_layout)

        # --- Таблиця ---
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Пристрій", "Користувач", "Оцінка", "Коментар", "Дата"])

        # Виділяти весь рядок
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        # Дозволити виділення лише одного рядка одночасно
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setColumnHidden(0, True)
        self.table.setColumnWidth(1, 250)    
        self.table.setColumnWidth(2, 160)    
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 220)
        self.table.setColumnWidth(5, 120)

        self.layout.addWidget(self.table)

        # --- Події ---
        self.add_btn.clicked.connect(self.add_review)
        self.edit_btn.clicked.connect(self.edit_review)
        self.delete_btn.clicked.connect(self.delete_review)

        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        reviews = self.db.get_reviews()
        devices = {d.id: d.name for d in self.db.get_devices()}

        for r in reviews:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(r.id)))
            self.table.setItem(row, 1, QTableWidgetItem(devices.get(r.device_id, "Невідомо")))
            self.table.setItem(row, 2, QTableWidgetItem(r.username or ""))
            self.table.setItem(row, 3, QTableWidgetItem(str(r.rating or "")))
            self.table.setItem(row, 4, QTableWidgetItem(r.comment or ""))
            self.table.setItem(row, 5, QTableWidgetItem(r.date or ""))

    def add_review(self):
        dialog = ReviewDialog(self.db)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            review = Review(**data)
            self.db.add_review(review)
            self.load_data()

    def edit_review(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Помилка", "Оберіть рядок для редагування")
            return
        review_id = int(self.table.item(row, 0).text())
        review = next((r for r in self.db.get_reviews() if r.id == review_id), None)
        if not review:
            return

        dialog = ReviewDialog(self.db, review)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            review.device_id = data["device_id"]
            review.username = data["username"]
            review.rating = data["rating"]
            review.comment = data["comment"]
            review.date = data["date"]
            self.db.update_review(review)
            self.load_data()

    def delete_review(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Помилка", "Оберіть рядок для видалення")
            return
        review_id = int(self.table.item(row, 0).text())
        confirm = QMessageBox.question(
            self, "Підтвердити", f"Видалити відгук ID {review_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.db.delete_review(review_id)
            self.load_data()

