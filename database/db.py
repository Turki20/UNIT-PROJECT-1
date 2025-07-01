
import sqlite3
# import csv
# from datetime import datetime 
# from models import Product

#from database.models import Transaction, Product, User, Report
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
    
    
# # قراءة ملف CSV
# with open('Products.csv', newline='', encoding='utf-8') as csvfile:
#     reader = csv.DictReader(csvfile)
#     products = []
#     count = 0

#     for row in reader:
#         if count >= 100:
#             break

#         name = row['Product Name']
#         desc = row['Brand Desc']
#         category_id = 0 
#         price_per_unit = float(row['SellPrice'])
#         tax_rate = 0.15
#         now = datetime.now().strftime('%Y-%m-%d %H:%M')
#         quantity = 0

#         product = Product(
#             name=name,
#             desc=desc,
#             category_id=category_id,
#             price_per_unit=price_per_unit,
#             tax_rate=tax_rate,
#             created_at=now,
#             updated_at=now,
#             quantity=quantity
#         )

#         products.append(product)
#         count += 1


# # إضافة المنتجات لقاعدة البيانات
# for product in products:
#     query = product.add_product_query()
#     execute(query)

# # إغلاق قاعدة البيانات
# clost_db()

# print("تمت إضافة 100 منتج بنجاح.")
    
    
    
# def initial_database():
#     execute(Report.create_table_query())
#     execute(Transaction.create_table_query())
#     execute(User.create_table_query())
#     execute(Product.create_table_query())
    
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


# from models import Report

# execute(Report.create_table_query())

# new_report = Report("test", "test content", "12/12/2020", 7)
# execute(new_report.add_report_query())


# report = Report.convert_to_Reports(get_all(Report.get_report_by_id_query(3)))[0]
# print(get_all(Report.get_all_reports_query()))

# print(report.created_at)
