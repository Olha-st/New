from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QVBoxLayout, QPushButton
from models import FAQ

class FAQDialog(QDialog):
    def __init__(self, db, faq=None):
        super().__init__()
        self.db = db
        self.faq = faq
        self.setWindowTitle("FAQ")
        self.setFixedWidth(300)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Вибір пристрою (0 або None = загальне)
        self.device_combo = QComboBox()
        self.device_combo.addItem("Загальне", None)
        for d in self.db.get_devices():
            self.device_combo.addItem(d.name, d.id)
        form_layout.addRow("Пристрій:", self.device_combo)

        self.question_edit = QLineEdit()
        form_layout.addRow("Питання:", self.question_edit)

        self.answer_edit = QLineEdit()
        form_layout.addRow("Відповідь:", self.answer_edit)

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

        if faq:
            self.device_combo.setCurrentIndex(
                self.device_combo.findData(faq.device_id)
            )
            self.question_edit.setText(faq.question or "")
            self.answer_edit.setText(faq.answer or "")

    def get_data(self):
        return {
            "device_id": self.device_combo.currentData(),
            "question": self.question_edit.text(),
            "answer": self.answer_edit.text()
        }
