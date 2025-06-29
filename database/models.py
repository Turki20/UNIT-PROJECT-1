
from datetime import datetime

class Product():
        
    def __init__(self, name:str, desc:str, category_id:int, price_per_unit:float, tax_rate:float, created_at:datetime, updated_at:datetime, quantity:int = 0, id:int=None):
        self.id = id
        self.name = name
        self.desc = desc
        self.category_id = category_id
        self.quantity = quantity
        self.price_per_unit = price_per_unit
        self.tax_rate = tax_rate
        self.created_at = created_at
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
    