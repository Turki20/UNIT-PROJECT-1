from textual.screen import Screen
from textual.widgets import Static, Rule, DataTable, Input, Button, Select
from textual.containers import Container, ScrollableContainer
from textual import on
from datetime import datetime
from database.models import Transaction, Product, Report
from database.db import execute, get_all
from user.session import Session
import csv
import os

def generate_invoice_csv(transaction: Transaction, product_name: str, save_dir="invoices"):
    os.makedirs(save_dir, exist_ok=True)

    filename = f"{save_dir}/invoice_{transaction.transaction_type}_{transaction.transaction_date.replace('/', '-')}_{transaction.product_id}.csv"
    
    with open(filename, mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Transaction Type", "Product", "Quantity", "Unit Price", "Total Price", "Tax Amount", "Date", "User ID"])
        writer.writerow([
            "Purchase" if transaction.transaction_type == "IN" else "Sale",
            product_name,
            transaction.quantity,
            transaction.unit_price,
            transaction.total_price,
            transaction.tax_amount,
            transaction.transaction_date,
            transaction.user_id
        ])
    return filename

def create_transaction_report(file_path, type, user_id=None):
    content = f"Saved in: {file_path}" # edit --
    created_at = datetime.now().strftime("%d/%m/%Y")
    report = Report(f"invoice: {type}", content, created_at, user_id)
    execute(report.add_report_query())

class AddTransaction(Screen):

    @on(Select.Changed, "#transaction_type")
    def handle_transaction_type_change(self, event):
        unit_price_input = self.query_one("#unit_price")
        if event.value == "OUT":
            unit_price_input.disabled = True 
            unit_price_input.value = ""  
        else:
            unit_price_input.disabled = False
            
    @on(Button.Pressed, "#cancelTransaction")
    def back_to_previous_page(self):
        self.app.pop_screen()

    @on(Button.Pressed, "#addTransaction")
    def add_transaction_to_database(self):
        try:
            transaction_type = self.query_one("#transaction_type").value
            product_id = int(self.query_one("#product_id").value)
            quantity = int(self.query_one("#quantity").value)
            user_id = Session.current_user.id
            invoice_file_path = ""

            
            product = Product.convert_to_Products(get_all(Product.get_product_by_id_query(product_id)))
            if not product:
                raise Exception("Product ID not found.")

            product = product[0]
            current_quantity = product.quantity
            
            if transaction_type == "OUT":
                if quantity > current_quantity:
                    raise Exception(f"Not enough stock. Available: {current_quantity}")
                unit_price = product.price_per_unit  # السعر من المنتج
                product.set_quantity(current_quantity - quantity)
            else:
                unit_price = float(self.query_one("#unit_price").value)
                product.set_quantity(current_quantity + quantity)
                new_price_per_unit = (current_quantity * product.price_per_unit + quantity * unit_price) / (quantity + current_quantity)
                product.set_price_per_unit(new_price_per_unit)
                
        
            tax_amount = quantity * unit_price *  0.15 # اخذ الضريبه من المنتج
            total_price = (quantity * unit_price) + tax_amount
                
            execute(product.update_product_query())

            new_transaction = Transaction(
                transaction_type=transaction_type,
                product_id=product_id,
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price,
                tax_amount=tax_amount,
                transaction_date=datetime.now().strftime("%d/%m/%Y"),
                user_id=user_id,
                invoice_file_path=invoice_file_path
            )

            execute(new_transaction.add_transaction_query())

            file_path = generate_invoice_csv(new_transaction, product.name)

            new_transaction.set_invoice_file_path(file_path)
            execute(f'''
                UPDATE transaction_table
                SET invoice_file_path = '{file_path}'
                WHERE transaction_id = (SELECT MAX(transaction_id) FROM transaction_table);
            ''')

            create_transaction_report(file_path, new_transaction.transaction_type,Session.current_user.id)

            msg = self.query_one("#msg", Static)
            msg.set_class(False, "error")
            msg.set_class(True, "message")
            msg.update("Transaction added successfully.")

        except Exception as e:
            msg = self.query_one("#msg", Static)
            msg.set_class(True, "error")
            msg.set_class(False, "message")
            msg.update(f"{e}")
        
    def compose(self):
        with Container(id="header"):
            yield Static("Inventory Management System", id="Title")
            yield Static("Record Sale Transaction", id="pageTitle")

        with ScrollableContainer(classes="container"):
            yield Static("Transaction Type: ", classes="label")
            yield Select(
                options=[
                    ("Sale (OUT)", "OUT"),
                    ("Purchase (IN)", "IN")
                ],
                id="transaction_type"
            )
            yield Static("Product ID: ", classes="label")
            yield Input(placeholder="Product ID", id="product_id", type="integer")
            yield Static("Quantity: ", classes="label")
            yield Input(placeholder="Quantity", id="quantity", type="integer")
            yield Static("Unit Price: ", classes="label")
            yield Input(placeholder="Unit Price", id="unit_price", type="number")

        with Container(classes="h justfybetween"):
            yield Button("Back", variant="error", classes="w_m", id="cancelTransaction")
            yield Static()
            yield Static("", classes="error", id="msg")
            yield Static()
            yield Button("Submit", variant="primary", classes="w_m", id="addTransaction")
