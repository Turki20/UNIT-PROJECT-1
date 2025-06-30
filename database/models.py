
from datetime import datetime

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
                updated_at = '{self.updated_at}'
            WHERE id = {self.id};
        '''
        return q
    
class User():
    
    roles = ["Admin", "InventoryStaff", "ReadOnly"]
    
    def __init__(self, username:str, password:str, full_name:str, email:str, created_at:datetime, updated_at:datetime, role:str=roles[2], id:int=None):
        self.username = username
        self.password = password
        self.full_name = full_name
        self.role = role
        self.email = email
        self.created_at = created_at
        self.updated_at = updated_at
        self.id = id
    
    
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
    