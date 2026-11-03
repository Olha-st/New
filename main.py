# main.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
from database import DatabaseManager

# Імпорт вкладок (пізніше реалізуємо в окремих файлах)
from tabs.devices_tab import DevicesTab
from tabs.specifications_tab import SpecificationsTab
from tabs.reviews_tab import ReviewsTab
from tabs.images_tab import ImagesTab
from tabs.faq_tab import FAQTab
from tabs.news_tab import NewsTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Інформаційний додаток: Принтери та Сканери")
        self.setGeometry(100, 100, 1300, 600)

        # Підключення до бази даних
        self.db = DatabaseManager()

        

        # Створюємо головний віджет і вкладки
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Додаємо вкладки
        self.init_tabs()

    def init_tabs(self):
        self.tabs.addTab(DevicesTab(self.db), "Пристрої")
        self.tabs.addTab(SpecificationsTab(self.db), "Характеристики")
        self.tabs.addTab(ReviewsTab(self.db), "Відгуки")
        self.tabs.addTab(ImagesTab(self.db), "Зображення")
        self.tabs.addTab(FAQTab(self.db), "FAQ")
        self.tabs.addTab(NewsTab(self.db), "Новини")

    def closeEvent(self, event):
        # Закриваємо підключення до бази при виході
        self.db.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Застосування стилю
    with open("style.qss", "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
