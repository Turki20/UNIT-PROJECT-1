
from textual.screen import Screen
from textual.widgets import Static, DataTable, Input, Button, TextArea
from textual.containers import ScrollableContainer, Container
from database.db import execute, get_all, clost_db
from database.models import Product
from textual import on
from database.models import Product
from datetime import datetime
    
class ViewProductsScreen(Screen):
    BINDINGS = [
        ("b", "go_back", "Back to Home"),
        ("1", "add_product", "add product"),
        ("2", "delete_product", "delete product"),
        ("3", "update_product", "update product"),
    ]
    
    def compose(self):
        with Container(id="header"):
            yield Static("Inventory Management System", id="Title")
            yield Static("Product Management", id="pageTitle")
        
        with ScrollableContainer(classes="container products"):
            yield DataTable()
        
        with Container(classes="h"):
            with Container(classes="subcontainer"):
                yield Static("1. Add a Product")
                yield Static("2. Delete a Product")
                yield Static("3. Update a Product")
            with Container(classes="subcontainer"):
                yield Static("4. Search for a Product", classes="gray")
                yield Static("5. Categorize Products", classes="gray")
            
        with Container(classes="footer"):
            yield Static("Choose what you want by pressing the appropriate number on the keyboard.")
            yield Static("Press 'b' to go back", classes="label")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("id", "name", "category id", "quantity", "price/unit", "tax rate", "created at", "updated at", "description")
        all = get_all(Product.get_all_products_query())
        products = Product.convert_to_Products(all)
        new_list = []
        for product in products:
            new_list.append((product.id, product.name, product.category_id, product.quantity, product.price_per_unit, product.tax_rate, product.created_at, product.updated_at, product.desc[:50] + "..." if len(product.desc) > 50 else product.desc))
        table.add_rows(new_list)
        
    def action_go_back(self):
        self.app.pop_screen()
        
    def action_add_product(self):
        self.app.push_screen(AddProduct())
        
    def action_delete_product(self):
        self.app.push_screen(DeleteProduct())
        
    def action_update_product(self):
        self.app.push_screen(UpdateProduct())
        
class DeleteProduct(Screen):
    msg_status = False
    @on(Button.Pressed, "#Delete")
    def delete_product(self):
        if not DeleteProduct.msg_status:
            msg = self.query_one("#msg")
            msg.set_class(False, "hide")
            msg.set_class(True, "block")
            DeleteProduct.msg_status = True
        else:
            msg = self.query_one("#msg")
            msg.set_class(True, "hide")
            msg.set_class(False, "block")
            DeleteProduct.msg_status = False
        
    @on(Button.Pressed, "#back")
    def back_to_product_screen(self):
        self.app.pop_screen()
    
    @on(Button.Pressed, "#yes")
    def delete(self):
        product_id = self.query_one("#product_id").value
        try:
            product_id = int(product_id)
            if len(get_all(Product.get_product_by_id_query(product_id))) == 0: raise Exception("ID Not Exist!. ")
            execute(Product.delete_product_query(product_id))
            self.app.pop_screen()
        except Exception as e:
            msg = self.query_one("#feedback")
            msg.update(f"{e}")
            msg = self.query_one("#msg")
            msg.set_class(True, "hide")
            msg.set_class(False, "block")
            DeleteProduct.msg_status = False
    
    def compose(self):
        with Container(classes="container center"):
            yield Static("Enter the Prduct ID", classes="label")
            yield Input(placeholder="ID", id="product_id", type="integer")
            with Container(classes="h justfybetween"):
                yield Button("Back", classes="w_m", id="back")
                yield Static()
                yield Static(id="feedback", classes="error")
                yield Static()
                yield Button("Delete", id="Delete", variant="error", classes="w_m")
            with Container(classes="warning hide", id="msg"):
                yield Static("Are you sure you want to delete?")
                yield Button("Yes", variant="error", id="yes")

class UpdateProduct(Screen):
    
    @on(Button.Pressed, "#back_to_main")
    @on(Button.Pressed, "#back")
    def back_to_product_screen(self):
        self.app.pop_screen()
        
    @on(Button.Pressed)
    def update_btn(self):
        try:
            product_id = int(self.query_one("#product_id").value)

            product = Product.convert_to_Products(get_all(Product.get_product_by_id_query(product_id)))[0]

            new_name = self.query_one("#name_input").value
            new_desc = self.query_one("#desc_input").text
            new_category = int(self.query_one("#category_input").value)
            new_quantity = int(self.query_one("#quantity_input").value)
            new_price = float(self.query_one("#price_input").value)
            new_tax = float(self.query_one("#tax_input").value)

            product.set_name(new_name)
            product.set_desc(new_desc)
            product.set_category_id(new_category)
            product.set_quantity(new_quantity)
            product.set_price_per_unit(new_price)
            product.set_tax_rate(new_tax)
            
            execute(product.update_product_query())

            msg = self.query_one("#feedback2")
            msg.update("Updated successfully")
            msg.set_class(True, "message")
            msg.set_class(False, "error")

        except Exception as e:
            # عرض رسالة خطأ
            msg = self.query_one("#feedback2")
            msg.update(f" {e}")
            msg.set_class(True, "error")
            msg.set_class(False, "message")
    
    @on(Button.Pressed, "#search")
    def update_product(self):
        product_id = self.query_one("#product_id").value
        try:
            product_id = int(product_id)
            product = get_all(Product.get_product_by_id_query(product_id))
            if len(product) == 0: raise Exception("ID Not Exist!. ")
            self.query_one("#container").set_class(True, "hide")
            cont = self.query_one("#container2")
            cont.set_class(False, "hide")
            cont.set_class(True, "block")
            
            product = product[0]
            self.query_one("#name_input").value = product[1]
            self.query_one("#desc_input").text = product[2]
            self.query_one("#category_input").value = str(product[3])
            self.query_one("#quantity_input").value = str(product[4])
            self.query_one("#price_input").value = str(product[5])
            self.query_one("#tax_input").value = str(product[6])
            
        except Exception as e:
            msg = self.query_one("#feedback")
            msg.update(f"{e}")
            cont = self.query_one("#container2")
            cont.set_class(True, "hide")
            cont.set_class(False, "block")
            
    
    def compose(self):
        with Container(classes="container", id="container"):
            yield Static("Enter the Prduct ID", classes="label")
            yield Input(placeholder="ID", id="product_id", type="integer")
            with Container(classes="h justfybetween"):
                yield Button("Back", classes="w_m", id="back")
                yield Static()
                yield Static(id="feedback", classes="error")
                yield Static()
                yield Button("Search", id="search", variant="warning", classes="w_m") 
    
        with ScrollableContainer(classes="container hide", id="container2"):
            yield Static("Product Name: ", classes="label")
            yield Input(placeholder="Name", id="name_input")
            yield Static("Descruption: ", classes="label")
            yield TextArea(id="desc_input")
            yield Static("Category: ", classes="label")
            yield Input(placeholder="Category ID", id="category_input")
            yield Static("Price per unit: ", classes="label")
            yield Input(placeholder="Price per Unit", id="price_input")
            yield Static("Tax rate: ", classes="label")
            yield Input(placeholder="Tax Rate", id="tax_input")
            yield Static("Quantity: ", classes="label")
            yield Input(placeholder="Quantity", id="quantity_input")

            with Container(classes="h justfybetween"):
                yield Button("Back", classes="w_m", id="back_to_main")
                yield Button("Save Changes", id="update_btn", variant="success", classes="w_m")
                yield Static(id="feedback2", classes="error")
                   
class AddProduct(Screen):
    
    @on(Button.Pressed, "#cancelProduct")
    def back_to_previus_page(self):
        self.app.pop_screen()
    
    @on(Button.Pressed, "#addProduct")
    def add_product_to_database(self):
        name = self.query_one("#product_name").value
        desc = self.query_one("#desc", TextArea).text
        category_id = self.query_one("#category_id").value
        price_per_unit = self.query_one("#price_per_unit").value
        tax_rate = self.query_one("#tax_rate").value
        msg = self.query_one("#msg", Static)
        try:
            new_product = Product(name, desc, category_id, price_per_unit, tax_rate, datetime.now().strftime("%d/%m/%Y"), datetime.now().strftime("%d/%m/%Y"), quantity=0)
            execute(new_product.add_product_query())
            msg.set_class(False, "error")
            msg.set_class(True, "message")
            msg.update("Added successfully")

        except Exception as e:
            msg.set_class(True, "error")
            msg.set_class(False, "message")
            msg.update(f"{e}")
            

            
    def compose(self):
        with Container(id="header"):
            yield Static("Inventory Management System", id="Title")
            yield Static("Add Product Page", id="pageTitle")
            
        with ScrollableContainer(classes="container"):
            yield Static("Product Name: ", classes="label")
            yield Input(placeholder="Product name", id="product_name")
            yield Static("Description: ", classes="label")
            yield TextArea(id="desc")
            yield Static("Category: ", classes="label")
            yield Input(placeholder="category id", id="category_id", type="integer")
            yield Static("Price Per Unit: ", classes="label")
            yield Input(placeholder="Price per unit", id="price_per_unit", type="number")
            yield Static("Tax Rate: ", classes="label")
            yield Input(placeholder="Tax rate", id="tax_rate", type="number")
        with Container(classes="h justfybetween"):
            yield Button("Back", variant="error", classes="w_m", id="cancelProduct")
            yield Static()
            yield Static("", classes="error", id="msg")
            yield Static()
            yield Button("Submit", variant="primary", classes="w_m", id="addProduct")
            