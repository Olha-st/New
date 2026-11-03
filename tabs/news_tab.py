from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox, QDialog
)
from models import News
from dialogs.news_dialog import NewsDialog  # окремий діалог для новин

class NewsTab(QWidget):
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

        # Додаємо кнопки та вирівнюємо їх ліворуч
        self.button_layout.addWidget(self.add_btn)
        self.button_layout.addWidget(self.edit_btn)
        self.button_layout.addWidget(self.delete_btn)
        self.button_layout.addStretch()  # зайвий простір залишаємо справа

        self.layout.addLayout(self.button_layout)

        # --- Таблиця ---
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Заголовок", "Контент", "Дата"])
        # Виділяти весь рядок
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        # Дозволити виділення лише одного рядка одночасно
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setColumnHidden(0, True)

    
        self.table.setColumnWidth(1, 300)    
        self.table.setColumnWidth(2, 400)    
        self.table.setColumnWidth(3, 150)    
 

        self.layout.addWidget(self.table)

        # --- Події ---
        self.add_btn.clicked.connect(self.add_news)
        self.edit_btn.clicked.connect(self.edit_news)
        self.delete_btn.clicked.connect(self.delete_news)

        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        news_list = self.db.get_news()
        for n in news_list:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(n.id)))
            self.table.setItem(row, 1, QTableWidgetItem(n.title or ""))
            self.table.setItem(row, 2, QTableWidgetItem(n.content or ""))
            self.table.setItem(row, 3, QTableWidgetItem(n.date or ""))

    def add_news(self):
        dialog = NewsDialog(self.db)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            news = News(**data)
            self.db.add_news(news)
            self.load_data()

    def edit_news(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Помилка", "Оберіть рядок для редагування")
            return
        news_id = int(self.table.item(row, 0).text())
        n = next((x for x in self.db.get_news() if x.id == news_id), None)
        if not n:
            return
        dialog = NewsDialog(self.db, n)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            n.title = data["title"]
            n.content = data["content"]
            n.date = data["date"]
            self.db.update_news(n)
            self.load_data()

    def delete_news(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Помилка", "Оберіть рядок для видалення")
            return
        news_id = int(self.table.item(row, 0).text())
        confirm = QMessageBox.question(
            self, "Підтвердити", f"Видалити новину ID {news_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.db.delete_news(news_id)
            self.load_data()
