
from datetime import datetime

class Product():
    
    def __init__(self, id:int, name:str, desc:str, category_id:int, quantity:int, price_per_unit:float, tax_rate:float, created_at:datetime, updated_at:datetime):
        self.id = id
        self.name = name
        self.desc = desc
        pass
    
    def add_product_query(self, product) -> str:
        '''
            return sql query for insert product
        '''
        pass