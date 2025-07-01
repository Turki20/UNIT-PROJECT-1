
from datetime import datetime
#from database.db import get_all

class Product():
        
    def __init__(self, name:str, desc:str, category_id:int, price_per_unit:float, tax_rate:float, created_at:datetime, updated_at:datetime, quantity:int = 0, id:int=None):
        self.id = id
        self.set_name(name)
        self.set_desc(desc)
        self.set_category_id(category_id)
        self.set_quantity(quantity)
        self.set_price_per_unit(price_per_unit)
        self.set_tax_rate(tax_rate)
        self.set_created_at(created_at)
        self.set_updated_at(updated_at)
        
    
    # ===== Setters with Validation =====

    def set_name(self, name:str):
        if not isinstance(name, str) or not name.strip() or len(name) < 2:
            raise ValueError("Product name must be a non-empty string.")
        self.name = name.strip()

    def set_desc(self, desc:str):
        if not isinstance(desc, str) or len(desc) < 3:
            raise ValueError("Description must be a string.")
        self.desc = desc.strip()

    def set_category_id(self, category_id:int):
        category = int(category_id)
        if not isinstance(category, int) or category < 0: # تحتاج التحقق من جهه جدول الفئات
            raise ValueError("Category ID must be a positive integer.")
        self.category_id = category

    def set_quantity(self, quantity:int):
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a positive integer.")
        self.quantity = quantity

    def set_price_per_unit(self, price_per_unit:float):
        price_per_unit = float(price_per_unit)
        if not isinstance(price_per_unit, (int, float)) or price_per_unit < 0:
            raise ValueError("Price per unit must be a positive number.")
        self.price_per_unit = float(price_per_unit)

    def set_tax_rate(self, tax_rate:float):
        tax_rate = float(tax_rate)
        if not isinstance(tax_rate, (int, float)) or not (0 <= tax_rate <= 1):
            raise ValueError("Tax rate must be a number between 0 and 1.")
        self.tax_rate = float(tax_rate)

    def set_created_at(self, created_at:datetime): # edit
        if not isinstance(created_at, str):
            raise ValueError("created_at must be a datetime object.")
        self.created_at = created_at

    def set_updated_at(self, updated_at:datetime): # edit
        if not isinstance(updated_at, str):
            raise ValueError("updated_at must be a datetime object.")
        self.updated_at = updated_at
    
    
    @staticmethod
    def create_table_query() -> str:
        q = '''
            CREATE TABLE IF NOT EXISTS product (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                desc TEXT,
                category_id INTEGER,
                quantity INTEGER,
                price_per_unit REAL,
                tax_rate REAL,
                created_at TEXT,
                updated_at TEXT
            );
        '''
        return q
    
    @staticmethod
    def delete_product_query(product_id:int) -> str:
        q = f'''
            DELETE FROM product
            WHERE id = {product_id};
        '''
        return q

    @staticmethod
    def get_all_products_query() -> str:
        q = '''
            SELECT * FROM product;
        '''
        return q

    @staticmethod
    def get_product_by_id_query(product_id:int) -> str:
        q = f'''
            SELECT * FROM product
            WHERE id = {product_id};
        '''
        return q
        
    @staticmethod
    def convert_to_Products(products:str) -> list:
        '''
        [(1, 'iphon 15', 'description', 0, 0, 4500.0, 0.15, '29/06/2025', '29/06/2025')]
        '''
        products_objects = []
        for product in products:
            new_product = Product(product[1], product[2], product[3], product[5], product[6],product[7] ,product[8],product[4], product[0])
            products_objects.append(new_product)
            
        return products_objects
    
    def add_product_query(self) -> str:
        q = f'''
            INSERT INTO product (name, desc, category_id, quantity, price_per_unit, tax_rate, created_at, updated_at)
            VALUES ('{self.name}', '{self.desc}', {self.category_id}, {self.quantity}, {self.price_per_unit}, {self.tax_rate}, '{self.created_at}', '{self.updated_at}');
        '''
        return q

    def update_product_query(self) -> str:
        q = f'''
            UPDATE product
            SET name = '{self.name}',
                desc = '{self.desc}',
                category_id = {self.category_id},
                quantity = {self.quantity},
                price_per_unit = {self.price_per_unit},
                tax_rate = {self.tax_rate},
                updated_at = '{datetime.now().strftime("%d/%m/%Y")}'
            WHERE id = {self.id};
        '''
        return q
    
class User():
    
    roles = ["Admin", "InventoryStaff", "ReadOnly"]
    
    def __init__(self, username: str, password: str, full_name: str, email: str,
                 created_at: str, updated_at: str, role: str = roles[2], id: int = None):
        self.set_username(username)
        self.set_password(password)
        self.set_full_name(full_name)
        self.set_email(email)
        self.set_role(role)
        self.set_created_at(created_at)
        self.set_updated_at(updated_at)
        self.id = id

    # ===== Setters with Validation =====
    def set_username(self, username: str):
        if not isinstance(username, str) or len(username.strip()) < 3:
            raise ValueError("Username must be at least 3 characters.")
        self.username = username.strip()

    def set_password(self, password: str):
        if not isinstance(password, str) or len(password) < 5:
            raise ValueError("Password must be at least 5 characters.")
        self.password = password

    def set_full_name(self, full_name: str):
        if not isinstance(full_name, str) or len(full_name.strip()) < 5:
            raise ValueError("Full name must be at least 5 characters.")
        self.full_name = full_name.strip()

    def set_email(self, email: str):
        if not isinstance(email, str) or "@" not in email or "." not in email:
            raise ValueError("Invalid email address.")
        self.email = email.strip()

    def set_role(self, role: str):
        if role not in User.roles:
            raise ValueError(f"Role must be one of: {', '.join(User.roles)}")
        self.role = role

    def set_created_at(self, created_at: str):
        if not isinstance(created_at, str):
            raise ValueError("created_at must be a string date.")
        self.created_at = created_at

    def set_updated_at(self, updated_at: str):
        if not isinstance(updated_at, str):
            raise ValueError("updated_at must be a string date.")
        self.updated_at = updated_at
    
    
    @staticmethod
    def create_table_query() -> str:
        q = '''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TEXT,
                updated_at TEXT
            );
        '''
        return q

    def add_user_query(self) -> str:
        q = f'''
            INSERT INTO user (username, password, full_name, email, role, created_at, updated_at)
            VALUES ('{self.username}', '{self.password}', '{self.full_name}', '{self.email}', '{self.role}', '{self.created_at}', '{self.updated_at}');
        '''
        return q

    def update_user_query(self) -> str:
        q = f'''
            UPDATE user
            SET username = '{self.username}',
                password = '{self.password}',
                full_name = '{self.full_name}',
                email = '{self.email}',
                role = '{self.role}',
                updated_at = '{self.updated_at}'
            WHERE id = {self.id};
        '''
        return q

    @staticmethod
    def delete_user_query(user_id:int) -> str:
        q = f'''
            DELETE FROM user
            WHERE id = {user_id};
        '''
        return q

    @staticmethod
    def get_all_users_query() -> str:
        q = '''
            SELECT * FROM user;
        '''
        return q

    @staticmethod
    def get_user_by_id_query(user_id:int) -> str:
        q = f'''
            SELECT * FROM user
            WHERE id = {user_id};
        '''
        return q

    @staticmethod
    def convert_to_Users(users:list) -> list:
        '''
        [(1, 'turki', '12345', 'Turki Almutairi', 'turki@example.com', 'Admin', '2025-06-29', '2025-06-29')]
        '''
        users_objects = []
        for user in users:
            new_user = User(
                username=user[1],
                password=user[2],
                full_name=user[3],
                email=user[4],
                role=user[5],
                created_at=user[6],
                updated_at=user[7],
                id=user[0]
            )
            users_objects.append(new_user)
        return users_objects
    
    @staticmethod
    def check_username_is_exist(username:str):
        if not isinstance(username, str) or len(username.strip()) < 3:
            raise ValueError("Username must be a non-empty string of at least 3 characters.")

        # تحقق من قاعدة البيانات: هل يوجد مستخدم بنفس الاسم؟
        existing_users = get_all(f"SELECT * FROM user WHERE username = '{username}'")

        # لو فيه مستخدم بنفس الاسم ID غير حالي — ارفض
        if len(existing_users) > 0:
            raise ValueError("Username already exists. Please choose a different one.")

        return False
    
class Transaction:
    
    def __init__(self, transaction_type:str, product_id:int, quantity:int, unit_price:float, total_price:float, tax_amount:float, transaction_date:datetime, user_id:int, invoice_file_path:str, transaction_id:int=None):
        self.transaction_id = transaction_id
        self.set_transaction_type(transaction_type)
        self.set_product_id(product_id)
        self.set_quantity(quantity)
        self.set_unit_price(unit_price)
        self.set_total_price(total_price)
        self.set_tax_amount(tax_amount)
        self.set_transaction_date(transaction_date)
        self.set_user_id(user_id)
        self.set_invoice_file_path(invoice_file_path)

    # ===== Setters with Validation =====

    def set_transaction_type(self, transaction_type:str):
        valid_types = ["IN", "OUT"]
        if transaction_type not in valid_types:
            raise ValueError(f"Transaction type must be one of {valid_types}.")
        self.transaction_type = transaction_type

    def set_product_id(self, product_id:int):
        if not isinstance(product_id, int) or product_id < 0:
            raise ValueError("Product ID must be a positive integer.")
        self.product_id = product_id

    def set_quantity(self, quantity:int):
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a positive integer.")
        self.quantity = quantity

    def set_unit_price(self, unit_price:float):
        unit_price = float(unit_price)
        if unit_price < 0:
            raise ValueError("Unit price must be a positive number.")
        self.unit_price = unit_price

    def set_total_price(self, total_price:float):
        total_price = float(total_price)
        if total_price < 0:
            raise ValueError("Total price must be a positive number.")
        self.total_price = total_price

    def set_tax_amount(self, tax_amount:float):
        tax_amount = float(tax_amount)
        if tax_amount < 0:
            raise ValueError("Tax amount must be a positive number.")
        self.tax_amount = tax_amount

    def set_transaction_date(self, transaction_date:datetime):
        if not isinstance(transaction_date, str):
            raise ValueError("Transaction date must be a string.")
        self.transaction_date = transaction_date

    def set_user_id(self, user_id:int):
        if not isinstance(user_id, int) or user_id < 0:
            raise ValueError("User ID must be a positive integer.")
        self.user_id = user_id

    def set_invoice_file_path(self, invoice_file_path:str):
        if not isinstance(invoice_file_path, str):
            raise ValueError("Invoice file path must be a string.")
        self.invoice_file_path = invoice_file_path.strip()

    # ===== SQL Queries =====

    @staticmethod
    def create_table_query() -> str:
        q = '''
            CREATE TABLE IF NOT EXISTS transaction_table (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_type TEXT NOT NULL,
                product_id INTEGER,
                quantity INTEGER,
                unit_price REAL,
                total_price REAL,
                tax_amount REAL,
                transaction_date TEXT,
                user_id INTEGER,
                invoice_file_path TEXT
            );
        '''
        return q

    def add_transaction_query(self) -> str:
        q = f'''
            INSERT INTO transaction_table (transaction_type, product_id, quantity, unit_price, total_price, tax_amount, transaction_date, user_id, invoice_file_path)
            VALUES ('{self.transaction_type}', {self.product_id}, {self.quantity}, {self.unit_price}, {self.total_price}, {self.tax_amount}, '{self.transaction_date}', {self.user_id}, '{self.invoice_file_path}');
        '''
        return q

    @staticmethod
    def delete_transaction_query(transaction_id:int) -> str:
        q = f'''
            DELETE FROM transaction_table
            WHERE transaction_id = {transaction_id};
        '''
        return q

    @staticmethod
    def get_all_transactions_query() -> str:
        q = '''
            SELECT * FROM transaction_table;
        '''
        return q

    @staticmethod
    def get_transaction_by_id_query(transaction_id:int) -> str:
        q = f'''
            SELECT * FROM transaction_table
            WHERE transaction_id = {transaction_id};
        '''
        return q

    @staticmethod
    def convert_to_Transactions(transactions:list) -> list:
        transaction_objects = []
        for t in transactions:
            new_transaction = Transaction(
                t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[0]
            )
            transaction_objects.append(new_transaction)
        return transaction_objects

class Report:
    
    def __init__(self, report_type: str, content: str, created_at: str, created_by: int = None, report_id: int = None):
        self.report_id = report_id
        self.set_report_type(report_type)
        self.set_content(content)
        self.set_created_at(created_at)
        self.set_created_by(created_by)

    # ===== Setters with Validation =====
    
    def set_report_type(self, report_type: str):
        if not isinstance(report_type, str) or report_type.strip() == "":
            raise ValueError("Report type must be a non-empty string.")
        self.report_type = report_type.strip()

    def set_content(self, content: str):
        if not isinstance(content, str) or content.strip() == "":
            raise ValueError("Content must be a non-empty string.")
        self.content = content.strip()

    def set_created_at(self, created_at: str):
        if not isinstance(created_at, str) or created_at.strip() == "":
            raise ValueError("Created_at must be a valid string (date).")
        self.created_at = created_at.strip()

    def set_created_by(self, created_by: int):
        if created_by is not None and (not isinstance(created_by, int) or created_by < 0):
            raise ValueError("Created_by must be a positive integer or None.")
        self.created_by = created_by

    # ===== SQL Queries =====

    @staticmethod
    def create_table_query() -> str:
        q = '''
            CREATE TABLE IF NOT EXISTS report (
                report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_type TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                created_by INTEGER
            );
        '''
        return q

    def add_report_query(self) -> str:
        created_by_value = "NULL" if self.created_by is None else str(self.created_by)
        q = f'''
            INSERT INTO report (report_type, content, created_at, created_by)
            VALUES ('{self.report_type}', '{self.content}', '{self.created_at}', {created_by_value});
        '''
        return q

    @staticmethod
    def delete_report_query(report_id: int) -> str:
        q = f'''
            DELETE FROM report
            WHERE report_id = {report_id};
        '''
        return q

    @staticmethod
    def get_all_reports_query() -> str:
        q = '''
            SELECT * FROM report;
        '''
        return q

    @staticmethod
    def get_report_by_id_query(report_id: int) -> str:
        q = f'''
            SELECT * FROM report
            WHERE report_id = {report_id};
        '''
        return q

    @staticmethod
    def convert_to_Reports(reports: list) -> list:
        '''
        Example:
        [
            (1, 'Sales Report', 'Content here...', '2024-06-20', 3),
            (2, 'Inventory Summary', 'Inventory details...', '2024-06-21', None)
        ]
        '''
        report_objects = []
        for r in reports:
            new_report = Report(
                r[1], r[2], r[3], r[4], r[0]
            )
            report_objects.append(new_report)
        return report_objects
