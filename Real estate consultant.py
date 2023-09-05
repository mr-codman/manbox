import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget, QVBoxLayout, QWidget

# تابعی برای ایجاد جدول در پایگاه داده اگر وجود نداشته باشد
def create_table():
    connection = sqlite3.connect('real_estate.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS properties
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       property_type TEXT,
                       location TEXT,
                       budget TEXT,
                       owner TEXT,
                       address TEXT,
                       area TEXT,
                       contact TEXT)''')
    connection.commit()
    connection.close()

class RealEstateApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("سامانه مشاوره املاک")
        self.setGeometry(100, 100, 800, 600)

        # ایجاد تب
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # ایجاد نوار منو
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu("فایل")
        self.edit_menu = self.menu_bar.addMenu("ویرایش")

        # ایجاد عناصر ویژه
        self.property_list = QListWidget(self)
        self.layout.addWidget(self.property_list)

        self.load_button = QPushButton("بارگذاری مشخصات ملک‌ها", self)
        self.layout.addWidget(self.load_button)

        self.property_type_label = QLabel("نوع ملک:", self)
        self.property_type_input = QLineEdit(self)
        self.layout.addWidget(self.property_type_label)
        self.layout.addWidget(self.property_type_input)

        self.location_label = QLabel("موقعیت:", self)
        self.location_input = QLineEdit(self)
        self.layout.addWidget(self.location_label)
        self.layout.addWidget(self.location_input)

        self.budget_label = QLabel("بودجه:", self)
        self.budget_input = QLineEdit(self)
        self.layout.addWidget(self.budget_label)
        self.layout.addWidget(self.budget_input)

        self.owner_label = QLabel("مالک:", self)
        self.owner_input = QLineEdit(self)
        self.layout.addWidget(self.owner_label)
        self.layout.addWidget(self.owner_input)

        self.address_label = QLabel("آدرس:", self)
        self.address_input = QLineEdit(self)
        self.layout.addWidget(self.address_label)
        self.layout.addWidget(self.address_input)

        self.area_label = QLabel("مساحت (متر مربع):", self)
        self.area_input = QLineEdit(self)
        self.layout.addWidget(self.area_label)
        self.layout.addWidget(self.area_input)

        self.contact_label = QLabel("شماره تماس:", self)
        self.contact_input = QLineEdit(self)
        self.layout.addWidget(self.contact_label)
        self.layout.addWidget(self.contact_input)

        self.submit_button = QPushButton("ثبت ملک", self)
        self.layout.addWidget(self.submit_button)

        self.edit_button = QPushButton("ویرایش ملک", self)
        self.layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("حذف ملک", self)
        self.layout.addWidget(self.delete_button)

        self.result_text = QTextEdit(self)
        self.layout.addWidget(self.result_text)

        # تعیین رفتار دکمه‌ها
        self.load_button.clicked.connect(self.load_properties)
        self.submit_button.clicked.connect(self.submit_property)
        self.edit_button.clicked.connect(self.edit_property)
        self.delete_button.clicked.connect(self.delete_property)

    def load_properties(self):
        # اتصال به پایگاه داده و بارگذاری ملک‌ها
        connection = sqlite3.connect('real_estate.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM properties")
        properties = cursor.fetchall()
        connection.close()

        # نمایش مشخصات ملک‌ها در لیست
        self.property_list.clear()
        for property in properties:
            self.property_list.addItem(f"{property[1]} - {property[2]} - {property[3]}")

    def submit_property(self):
        # دریافت اطلاعات وارد شده توسط کاربر
        property_type = self.property_type_input.text()
        location = self.location_input.text()
        budget = self.budget_input.text()
        owner = self.owner_input.text()
        address = self.address_input.text()
        area = self.area_input.text()
        contact = self.contact_input.text()

        # اتصال به پایگاه داده و ذخیره اطلاعات ملک
        connection = sqlite3.connect('real_estate.db')
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO properties
                          (property_type, location, budget, owner, address, area, contact)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (property_type, location, budget, owner, address, area, contact))
        connection.commit()
        connection.close()

        self.result_text.setText(f"اطلاعات ملک با موفقیت ذخیره شد.")

    def edit_property(self):
        # دریافت شناسه ملک جهت ویرایش
        selected_item = self.property_list.currentItem()
        if selected_item:
            property_id = selected_item.text().split('-')[0].strip()
            property_type = self.property_type_input.text()
            location = self.location_input.text()
            budget = self.budget_input.text()
            owner = self.owner_input.text()
            address = self.address_input.text()
            area = self.area_input.text()
            contact = self.contact_input.text()

            # اتصال به پایگاه داده و ویرایش اطلاعات ملک
            connection = sqlite3.connect('real_estate.db')
            cursor = connection.cursor()
            cursor.execute('''UPDATE properties
                              SET property_type=?, location=?, budget=?, owner=?, address=?, area=?, contact=?
                              WHERE id=?''',
                           (property_type, location, budget, owner, address, area, contact, property_id))
            connection.commit()
            connection.close()

            self.result_text.setText(f"اطلاعات ملک با موفقیت ویرایش شد.")
        else:
            self.result_text.setText("لطفاً یک ملک را انتخاب کنید.")

    def delete_property(self):
        # دریافت شناسه ملک جهت حذف
        selected_item = self.property_list.currentItem()
        if selected_item:
            property_id = selected_item.text().split('-')[0].strip()

            # اتصال به پایگاه داده و حذف ملک
            connection = sqlite3.connect('real_estate.db')
            cursor = connection.cursor()
            cursor.execute("DELETE FROM properties WHERE id=?", (property_id,))
            connection.commit()
            connection.close()

            self.result_text.setText(f"ملک با موفقیت حذف شد.")
        else:
            self.result_text.setText("لطفاً یک ملک را انتخاب کنید.")

if __name__ == "__main__":
    create_table()
    app = QApplication(sys.argv)
    real_estate_app = RealEstateApp()
    real_estate_app.show()
    sys.exit(app.exec_())
