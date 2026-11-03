from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QSpinBox, QPushButton, QVBoxLayout, QComboBox, QDateEdit
from PyQt5.QtCore import QDate
from models import Review

class ReviewDialog(QDialog):
    def __init__(self, db, review=None):
        super().__init__()
        self.db = db
        self.review = review
        self.setWindowTitle("Відгук")
        self.setFixedWidth(300)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Вибір пристрою
        self.device_combo = QComboBox()
        for d in self.db.get_devices():
            self.device_combo.addItem(d.name, d.id)
        form_layout.addRow("Пристрій:", self.device_combo)

        self.username_edit = QLineEdit()
        form_layout.addRow("Користувач:", self.username_edit)

        self.rating_spin = QSpinBox()
        self.rating_spin.setRange(1, 5)
        form_layout.addRow("Оцінка:", self.rating_spin)

        self.comment_edit = QLineEdit()
        form_layout.addRow("Коментар:", self.comment_edit)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        form_layout.addRow("Дата:", self.date_edit)

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

        if review:
            self.device_combo.setCurrentIndex(
                self.device_combo.findData(review.device_id)
            )
            self.username_edit.setText(review.username or "")
            self.rating_spin.setValue(review.rating or 1)
            self.comment_edit.setText(review.comment or "")
            self.date_edit.setDate(QDate.fromString(review.date, "yyyy-MM-dd"))

    def get_data(self):
        return {
            "device_id": self.device_combo.currentData(),
            "username": self.username_edit.text(),
            "rating": self.rating_spin.value(),
            "comment": self.comment_edit.text(),
            "date": self.date_edit.date().toString("yyyy-MM-dd")
        }
