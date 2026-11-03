import sqlite3

# Підключення до бази даних
conn = sqlite3.connect("printers.db")
cursor = conn.cursor()

# ----------------------------
# Створення таблиць
# ----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS Manufacturers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country TEXT,
    website TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS DeviceTypes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    manufacturer_id INTEGER NOT NULL,
    device_type_id INTEGER NOT NULL,
    price REAL,
    stock_quantity INTEGER,
    description TEXT,
    FOREIGN KEY(manufacturer_id) REFERENCES Manufacturers(id),
    FOREIGN KEY(device_type_id) REFERENCES DeviceTypes(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Specifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id INTEGER NOT NULL,
    resolution TEXT,
    print_speed TEXT,
    scan_speed TEXT,
    color TEXT,
    interface TEXT,
    paper_size TEXT,
    duplex BOOLEAN,
    FOREIGN KEY(device_id) REFERENCES Devices(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id INTEGER NOT NULL,
    username TEXT,
    rating INTEGER,
    comment TEXT,
    date TEXT,
    FOREIGN KEY(device_id) REFERENCES Devices(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id INTEGER NOT NULL,
    file_path TEXT,
    description TEXT,
    FOREIGN KEY(device_id) REFERENCES Devices(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS FAQs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id INTEGER,
    question TEXT,
    answer TEXT,
    FOREIGN KEY(device_id) REFERENCES Devices(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS News (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT,
    date TEXT
)
""")

# ----------------------------
# Тестові дані
# ----------------------------

# Виробники
manufacturers = [
    ("HP", "США", "https://www.hp.com"),
    ("Canon", "Японія", "https://www.canon.com"),
    ("Epson", "Японія", "https://www.epson.com"),
    ("Brother", "Японія", "https://www.brother.com"),
    ("Samsung", "Південна Корея", "https://www.samsung.com"),
    ("Lexmark", "США", "https://www.lexmark.com"),
    ("Xerox", "США", "https://www.xerox.com"),
    ("Kyocera", "Японія", "https://www.kyocera.com")
]
cursor.executemany("INSERT INTO Manufacturers (name, country, website) VALUES (?, ?, ?)", manufacturers)

# Типи пристроїв
device_types = [
    ("Принтер", "Пристрій для друку документів"),
    ("Сканер", "Пристрій для сканування документів"),
    ("МФУ", "Багатофункційний пристрій (Друк/Скан/Копія)"),
    ("3D Принтер", "Пристрій для 3D друку")
]
cursor.executemany("INSERT INTO DeviceTypes (name, description) VALUES (?, ?)", device_types)

# Пристрої
devices = [
    ("HP LaserJet Pro M404dn", 1, 1, 250.0, 10, "Чорно-білий лазерний принтер"),
    ("Canon PIXMA TS6320", 2, 3, 150.0, 15, "Багатофункційний кольоровий принтер"),
    ("Epson EcoTank L3150", 3, 3, 180.0, 8, "МФУ з системою безперервної подачі чорнил"),
    ("Brother DCP-L2550DN", 4, 3, 220.0, 5, "Лазерне МФУ з двостороннім друком"),
    ("Samsung Xpress SL-M2835DW", 5, 1, 200.0, 12, "Компактний чорно-білий принтер"),
    ("Lexmark B2236dw", 6, 1, 180.0, 7, "Недорогий монохромний принтер"),
    ("Xerox VersaLink C400", 7, 1, 400.0, 4, "Кольоровий офісний принтер"),
    ("Kyocera ECOSYS P5026cdw", 8, 1, 350.0, 6, "Кольоровий лазерний принтер")
]
cursor.executemany("""
INSERT INTO Devices (name, manufacturer_id, device_type_id, price, stock_quantity, description)
VALUES (?, ?, ?, ?, ?, ?)
""", devices)

# Характеристики
specs = [
    (1, "1200x1200 dpi", "38 стор/хв", None, "Ч/Б", "USB/Ethernet", "A4", True),
    (2, "4800x1200 dpi", "15 стор/хв", None, "Кольоровий", "USB/Wi-Fi", "A4", False),
    (3, "5760x1440 dpi", "10 стор/хв", None, "Кольоровий", "USB/Wi-Fi", "A4", False),
    (4, "1200x1200 dpi", "30 стор/хв", None, "Ч/Б", "USB/Ethernet", "A4", True),
    (5, "1200x1200 dpi", "29 стор/хв", None, "Ч/Б", "USB/Wi-Fi", "A4", True),
    (6, "1200x1200 dpi", "26 стор/хв", None, "Ч/Б", "USB", "A4", False),
    (7, "1200x1200 dpi", "35 стор/хв", None, "Кольоровий", "USB/Ethernet", "A4", True),
    (8, "1200x1200 dpi", "28 стор/хв", None, "Кольоровий", "USB/Wi-Fi", "A4", True)
]
cursor.executemany("""
INSERT INTO Specifications (device_id, resolution, print_speed, scan_speed, color, interface, paper_size, duplex)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", specs)

# Відгуки
reviews = [
    (1, "Ольга", 5, "Відмінний принтер!", "2025-11-10"),
    (2, "Андрій", 4, "Хороша ціна та якість", "2025-11-09"),
    (3, "Софія", 5, "Обожнюю систему EcoTank", "2025-11-08"),
    (4, "Іван", 4, "Надійний принтер", "2025-11-07"),
    (5, "Марія", 3, "Трохи шумний", "2025-11-06"),
    (6, "Дмитро", 4, "Добре працює", "2025-11-05"),
    (7, "Катерина", 5, "Чудова кольоровий друк", "2025-11-04"),
    (8, "Тарас", 4, "Хороший офісний принтер", "2025-11-03")
]
cursor.executemany("""
INSERT INTO Reviews (device_id, username, rating, comment, date)
VALUES (?, ?, ?, ?, ?)
""", reviews)

# Зображення
images = [
    (1, "images/hp_m404dn.jpg", "Вигляд спереду"),
    (2, "images/canon_ts6320.jpg", "Принтер із лотком для паперу"),
    (3, "images/epson_l3150.jpg", "Система EcoTank"),
    (4, "images/brother_dcp.jpg", "МФУ спереду"),
    (5, "images/samsung_sl_m2835dw.jpg", "Компактний принтер"),
    (6, "images/lexmark_b2236dw.jpg", "Монохромний принтер"),
    (7, "images/xerox_c400.jpg", "Офісний кольоровий принтер"),
    (8, "images/kyocera_p5026cdw.jpg", "Лазерний принтер")
]
cursor.executemany("""
INSERT INTO Images (device_id, file_path, description)
VALUES (?, ?, ?)
""", images)

# FAQ
faqs = [
    (1, "Як замінити тонер?", "Відкрийте передню кришку, витягніть картридж, вставте новий."),
    (2, "Як підключити принтер по Wi-Fi?", "Використайте меню принтера або програму виробника."),
    (None, "Що таке двосторонній друк?", "Друк на обох сторонах аркуша автоматично."),
    (None, "Як часто чистити принтер?", "Рекомендовано раз на місяць."),
    (3, "Як заправити баки з чорнилом?", "Відкрийте бак і заправте сумісним чорнилом."),
    (4, "Як увімкнути двосторонній друк?", "Увімкніть відповідну опцію у налаштуваннях принтера."),
    (5, "Що робити при застряганні паперу?", "Обережно вийміть папір і перезапустіть принтер."),
    (6, "Як скинути налаштування принтера?", "Вимкніть і утримуйте кнопку скидання 5 секунд.")
]
cursor.executemany("""
INSERT INTO FAQs (device_id, question, answer)
VALUES (?, ?, ?)
""", faqs)

# Новини
news = [
    ("HP випустила новий LaserJet", "HP представила нову серію LaserJet M500 для офісів", "2025-11-01"),
    ("Canon оновлює PIXMA", "Canon оновила серію PIXMA TS з покращеною швидкістю", "2025-11-02"),
    ("Epson представляє EcoTank L400", "Нове МФУ з більшою ємністю чорнил", "2025-11-03"),
    ("Огляд MFP Brother", "Серія DCP протестована експертами", "2025-11-04"),
    ("Поради для Samsung Xpress", "Топ-поради для принтерів Samsung Xpress", "2025-11-05"),
    ("Lexmark B серія оновлення", "Доступне оновлення прошивки для Lexmark B", "2025-11-06"),
    ("Новини Xerox C серії", "Xerox VersaLink C400 доступний на нових ринках", "2025-11-07"),
    ("Kyocera: обслуговування принтерів", "Kyocera ділиться порадами з обслуговування", "2025-11-08")
]
cursor.executemany("""
INSERT INTO News (title, content, date)
VALUES (?, ?, ?)
""", news)

# ----------------------------
# Підтвердження та закриття
# ----------------------------
conn.commit()
conn.close()

print("База даних 'printers.db' створена та заповнена тестовими даними українською!")
