# models.py

# ----------------------------
# Виробники
# ----------------------------
class Manufacturer:
    def __init__(self, id=None, name="", country=None, website=None):
        self.id = id
        self.name = name
        self.country = country
        self.website = website

# ----------------------------
# Типи пристроїв
# ----------------------------
class DeviceType:
    def __init__(self, id=None, name="", description=None):
        self.id = id
        self.name = name
        self.description = description

# ----------------------------
# Пристрої
# ----------------------------
class Device:
    def __init__(self, id=None, name="", manufacturer_id=None, device_type_id=None, price=None, stock_quantity=None, description=None):
        self.id = id
        self.name = name
        self.manufacturer_id = manufacturer_id
        self.device_type_id = device_type_id
        self.price = price
        self.stock_quantity = stock_quantity
        self.description = description

# ----------------------------
# Характеристики
# ----------------------------
class Specification:
    def __init__(self, id=None, device_id=None, resolution=None, print_speed=None, scan_speed=None, color=None, interface=None, paper_size=None, duplex=False):
        self.id = id
        self.device_id = device_id
        self.resolution = resolution
        self.print_speed = print_speed
        self.scan_speed = scan_speed
        self.color = color
        self.interface = interface
        self.paper_size = paper_size
        self.duplex = duplex

# ----------------------------
# Відгуки / опитування
# ----------------------------
class Review:
    def __init__(self, id=None, device_id=None, username=None, rating=None, comment=None, date=None):
        self.id = id
        self.device_id = device_id
        self.username = username
        self.rating = rating
        self.comment = comment
        self.date = date

# ----------------------------
# Зображення
# ----------------------------
class Image:
    def __init__(self, id=None, device_id=None, file_path=None, description=None):
        self.id = id
        self.device_id = device_id
        self.file_path = file_path
        self.description = description

# ----------------------------
# FAQ / поради
# ----------------------------
class FAQ:
    def __init__(self, id=None, device_id=None, question=None, answer=None):
        self.id = id
        self.device_id = device_id
        self.question = question
        self.answer = answer

# ----------------------------
# Новини
# ----------------------------
class News:
    def __init__(self, id=None, title=None, content=None, date=None):
        self.id = id
        self.title = title
        self.content = content
        self.date = date
