# database.py

import sqlite3
from models import Manufacturer, DeviceType, Device, Specification, Review, Image, FAQ, News

class DatabaseManager:
    def __init__(self, db_name="printers.db"):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    # ----------------------------
    # CRUD для Manufacturer
    # ----------------------------
    def add_manufacturer(self, manufacturer: Manufacturer):
        self.cursor.execute(
            "INSERT INTO Manufacturers (name, country, website) VALUES (?, ?, ?)",
            (manufacturer.name, manufacturer.country, manufacturer.website)
        )
        self.conn.commit()
        manufacturer.id = self.cursor.lastrowid
        return manufacturer.id

    def get_manufacturers(self):
        self.cursor.execute("SELECT * FROM Manufacturers")
        return [Manufacturer(**row) for row in map(dict, self.cursor.fetchall())]

    def update_manufacturer(self, manufacturer: Manufacturer):
        self.cursor.execute(
            "UPDATE Manufacturers SET name=?, country=?, website=? WHERE id=?",
            (manufacturer.name, manufacturer.country, manufacturer.website, manufacturer.id)
        )
        self.conn.commit()

    def delete_manufacturer(self, manufacturer_id):
        self.cursor.execute("DELETE FROM Manufacturers WHERE id=?", (manufacturer_id,))
        self.conn.commit()

    # ----------------------------
    # CRUD для DeviceType
    # ----------------------------
    def add_device_type(self, device_type: DeviceType):
        self.cursor.execute(
            "INSERT INTO DeviceTypes (name, description) VALUES (?, ?)",
            (device_type.name, device_type.description)
        )
        self.conn.commit()
        device_type.id = self.cursor.lastrowid
        return device_type.id

    def get_device_types(self):
        self.cursor.execute("SELECT * FROM DeviceTypes")
        return [DeviceType(**row) for row in map(dict, self.cursor.fetchall())]

    def update_device_type(self, device_type: DeviceType):
        self.cursor.execute(
            "UPDATE DeviceTypes SET name=?, description=? WHERE id=?",
            (device_type.name, device_type.description, device_type.id)
        )
        self.conn.commit()

    def delete_device_type(self, device_type_id):
        self.cursor.execute("DELETE FROM DeviceTypes WHERE id=?", (device_type_id,))
        self.conn.commit()

    # ----------------------------
    # CRUD для Device
    # ----------------------------
    def add_device(self, device: Device):
        self.cursor.execute(
            "INSERT INTO Devices (name, manufacturer_id, device_type_id, price, stock_quantity, description) VALUES (?, ?, ?, ?, ?, ?)",
            (device.name, device.manufacturer_id, device.device_type_id, device.price, device.stock_quantity, device.description)
        )
        self.conn.commit()
        device.id = self.cursor.lastrowid
        return device.id

    def get_devices(self):
        self.cursor.execute("SELECT * FROM Devices")
        return [Device(**row) for row in map(dict, self.cursor.fetchall())]

    def update_device(self, device: Device):
        self.cursor.execute(
            "UPDATE Devices SET name=?, manufacturer_id=?, device_type_id=?, price=?, stock_quantity=?, description=? WHERE id=?",
            (device.name, device.manufacturer_id, device.device_type_id, device.price, device.stock_quantity, device.description, device.id)
        )
        self.conn.commit()

    def delete_device(self, device_id):
        self.cursor.execute("DELETE FROM Devices WHERE id=?", (device_id,))
        self.conn.commit()

    def get_device_by_id(self, device_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, name, manufacturer_id, device_type_id, price
            FROM Devices WHERE id = ?
        """, (device_id,))
        row = cursor.fetchone()
        if row:
            return Device(*row)
        return None
    
    def get_specification_by_device(self, device_id):
        self.cursor.execute("""
            SELECT * FROM Specifications WHERE device_id = ?
        """, (device_id,))
        row = self.cursor.fetchone()
        if row:
            from models import Specification
            return Specification(**dict(row))
        return None
    
    def get_images_by_device(self, device_id):
        self.cursor.execute("SELECT * FROM Images WHERE device_id = ?", (device_id,))
        rows = self.cursor.fetchall()
        if rows:
            from models import Image
            return [Image(**dict(r)) for r in rows]
        return []




    # ----------------------------
    # CRUD для Specification
    # ----------------------------
    def add_specification(self, spec: Specification):
        self.cursor.execute(
            "INSERT INTO Specifications (device_id, resolution, print_speed, scan_speed, color, interface, paper_size, duplex) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (spec.device_id, spec.resolution, spec.print_speed, spec.scan_speed, spec.color, spec.interface, spec.paper_size, spec.duplex)
        )
        self.conn.commit()
        spec.id = self.cursor.lastrowid
        return spec.id

    def get_specifications(self):
        self.cursor.execute("SELECT * FROM Specifications")
        return [Specification(**row) for row in map(dict, self.cursor.fetchall())]

    def update_specification(self, spec: Specification):
        self.cursor.execute(
            "UPDATE Specifications SET device_id=?, resolution=?, print_speed=?, scan_speed=?, color=?, interface=?, paper_size=?, duplex=? WHERE id=?",
            (spec.device_id, spec.resolution, spec.print_speed, spec.scan_speed, spec.color, spec.interface, spec.paper_size, spec.duplex, spec.id)
        )
        self.conn.commit()

    def delete_specification(self, spec_id):
        self.cursor.execute("DELETE FROM Specifications WHERE id=?", (spec_id,))
        self.conn.commit()

    # ----------------------------
    # CRUD для Review
    # ----------------------------
    def add_review(self, review: Review):
        self.cursor.execute(
            "INSERT INTO Reviews (device_id, username, rating, comment, date) VALUES (?, ?, ?, ?, ?)",
            (review.device_id, review.username, review.rating, review.comment, review.date)
        )
        self.conn.commit()
        review.id = self.cursor.lastrowid
        return review.id

    def get_reviews(self):
        self.cursor.execute("SELECT * FROM Reviews")
        return [Review(**row) for row in map(dict, self.cursor.fetchall())]

    def update_review(self, review: Review):
        self.cursor.execute(
            "UPDATE Reviews SET device_id=?, username=?, rating=?, comment=?, date=? WHERE id=?",
            (review.device_id, review.username, review.rating, review.comment, review.date, review.id)
        )
        self.conn.commit()

    def delete_review(self, review_id):
        self.cursor.execute("DELETE FROM Reviews WHERE id=?", (review_id,))
        self.conn.commit()

    # ----------------------------
    # CRUD для Image
    # ----------------------------
    def add_image(self, image: Image):
        self.cursor.execute(
            "INSERT INTO Images (device_id, file_path, description) VALUES (?, ?, ?)",
            (image.device_id, image.file_path, image.description)
        )
        self.conn.commit()
        image.id = self.cursor.lastrowid
        return image.id

    def get_images(self):
        self.cursor.execute("SELECT * FROM Images")
        return [Image(**row) for row in map(dict, self.cursor.fetchall())]

    def update_image(self, image: Image):
        self.cursor.execute(
            "UPDATE Images SET device_id=?, file_path=?, description=? WHERE id=?",
            (image.device_id, image.file_path, image.description, image.id)
        )
        self.conn.commit()

    def delete_image(self, image_id):
        self.cursor.execute("DELETE FROM Images WHERE id=?", (image_id,))
        self.conn.commit()

    # ----------------------------
    # CRUD для FAQ
    # ----------------------------
    def add_faq(self, faq: FAQ):
        self.cursor.execute(
            "INSERT INTO FAQs (device_id, question, answer) VALUES (?, ?, ?)",
            (faq.device_id, faq.question, faq.answer)
        )
        self.conn.commit()
        faq.id = self.cursor.lastrowid
        return faq.id

    def get_faqs(self):
        self.cursor.execute("SELECT * FROM FAQs")
        return [FAQ(**row) for row in map(dict, self.cursor.fetchall())]

    def update_faq(self, faq: FAQ):
        self.cursor.execute(
            "UPDATE FAQs SET device_id=?, question=?, answer=? WHERE id=?",
            (faq.device_id, faq.question, faq.answer, faq.id)
        )
        self.conn.commit()

    def delete_faq(self, faq_id):
        self.cursor.execute("DELETE FROM FAQs WHERE id=?", (faq_id,))
        self.conn.commit()

    # ----------------------------
    # CRUD для News
    # ----------------------------
    def add_news(self, news: News):
        self.cursor.execute(
            "INSERT INTO News (title, content, date) VALUES (?, ?, ?)",
            (news.title, news.content, news.date)
        )
        self.conn.commit()
        news.id = self.cursor.lastrowid
        return news.id

    def get_news(self):
        self.cursor.execute("SELECT * FROM News")
        return [News(**row) for row in map(dict, self.cursor.fetchall())]

    def update_news(self, news: News):
        self.cursor.execute(
            "UPDATE News SET title=?, content=?, date=? WHERE id=?",
            (news.title, news.content, news.date, news.id)
        )
        self.conn.commit()

    def delete_news(self, news_id):
        self.cursor.execute("DELETE FROM News WHERE id=?", (news_id,))
        self.conn.commit()

    # ----------------------------
    # Закриття підключення
    # ----------------------------
    def close(self):
        self.conn.close()
