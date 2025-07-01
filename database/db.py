
import sqlite3

# # connection object
# conn = sqlite3.connect("inventory.db") # انشاء الاتصال او انشاء ملف قاعدة البيانات
# # هو الاداة اللي تنفذ الاستعلامات
# cursor = conn.cursor() # اللي يسمح لك تكتب وتقرا وتنفذ العمليات في الداتا بيس 

# cursor.execute("q")

# # هذا مهم في حال عدلت على بيانات في قاعدة البيانات لو ماسويته ماراح تتخزن
# conn.commit()
# # هذا بعد تسوي سيليكت يرجع لك كل البيانات على شكل list of tuples
# cursor.fetchall()

# # اغلاق قاعدة البيانات بعد العمل
# conn.close()


conn = sqlite3.connect("database/inventory.db")
cursor = conn.cursor()

def execute(q:str):
    global conn
    global cursor
    cursor.execute(q)
    conn.commit()

def get_all(q:str):
    global cursor
    cursor.execute(q)
    return cursor.fetchall()

def clost_db():
    global conn
    conn.close()
    
    
def initial_database():
    pass

# cursor.execute(p1.add_product_query())
# conn.commit()

# cursor.execute(Product.delete_product_query(1))
# conn.commit()

# # execute(Product.create_table_query())
#from models import Product
# from datetime import datetime
# p = Product("iphon 14", "description", 0, 4500, 0.15, datetime.now().strftime("%d/%m/%Y"), datetime.now().strftime("%d/%m/%Y"))
# execute(p.add_product_query())

# execute(Product.delete_product_query(6))
# products = get_all(Product.get_all_products_query())
# print(products)
# result = Product.convert_to_Products(products)
# for i in result:
#     print(Product.get_product_by_id_query(i.id))
#     print(get_all(Product.get_product_by_id_query(i.id)))

# execute(User.create_table_query())

# user = User("turki", "12345678", "Turki Ahmed", "turki@gmail.com", datetime.now().strftime("%d/%m/%Y"), datetime.now().strftime("%d/%m/%Y"))
# execute(user.add_user_query())

# from models import Transaction

# execute(Transaction.create_table_query())

# t1 = Transaction(
#     transaction_type="IN",
#     product_id=1,
#     quantity=10,
#     unit_price=50.0,
#     total_price=500.0,
#     tax_amount=75.0,
#     transaction_date="29/06/2025",
#     user_id=2,
#     invoice_file_path="invoices/inv001.pdf"
# )

# # execute(t1.add_transaction_query())
# print(execute(Transaction.delete_transaction_query(1)))
# print(get_all(Transaction.get_all_transactions_query()))