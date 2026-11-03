from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QVBoxLayout, QPushButton, QDateEdit
from PyQt5.QtCore import QDate

class NewsDialog(QDialog):
    def __init__(self, db, news=None):
        super().__init__()
        self.db = db
        self.news = news
        self.setWindowTitle("Новина")
        self.setFixedWidth(350)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.title_edit = QLineEdit()
        form_layout.addRow("Заголовок:", self.title_edit)

        self.content_edit = QLineEdit()
        form_layout.addRow("Контент:", self.content_edit)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        form_layout.addRow("Дата:", self.date_edit)

        layout.addLayout(form_layout)

        self.save_btn = QPushButton("Зберегти")
        self.cancel_btn = QPushButton("Скасувати")
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        if news:
            self.title_edit.setText(news.title or "")
            self.content_edit.setText(news.content or "")
            if news.date:
                self.date_edit.setDate(QDate.fromString(news.date, "yyyy-MM-dd"))

    def get_data(self):
        return {
            "title": self.title_edit.text(),
            "content": self.content_edit.text(),
            "date": self.date_edit.date().toString("yyyy-MM-dd")
        }
