from textual.screen import Screen
from textual.widgets import Static, Rule, DataTable, Input, Button, Select
from textual.containers import Container, ScrollableContainer
from textual import on
from datetime import datetime
from database.models import Transaction, Product
from database.db import execute, get_all

class AddTransaction(Screen):

    @on(Button.Pressed, "#cancelTransaction")
    def back_to_previous_page(self):
        self.app.pop_screen()

    @on(Button.Pressed, "#addTransaction")
    def add_transaction_to_database(self):
        try:
            transaction_type = self.query_one("#transaction_type").value
            product_id = int(self.query_one("#product_id").value)
            quantity = int(self.query_one("#quantity").value)
            unit_price = float(self.query_one("#unit_price").value)
            tax_amount = 0.15 # اخذ الضريبه من المنتج
            user_id = 1
            invoice_file_path = self.query_one("#invoice_file_path").value

            total_price = (quantity * unit_price) + tax_amount

            product = Product.convert_to_Products(get_all(Product.get_product_by_id_query(product_id)))
            if not product:
                raise Exception("Product ID not found.")

            product = product[0]
            current_quantity = product.quantity
            if transaction_type == "OUT":
                if quantity > current_quantity:
                    raise Exception(f"Not enough stock. Available: {current_quantity}")
                product.set_quantity(current_quantity - quantity)
            else:  # IN
                product.set_quantity(current_quantity + quantity)
                
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
            yield Static("Invoice File Path: ", classes="label")
            yield Input(placeholder="Invoice Path (optional)", id="invoice_file_path")

        with Container(classes="h justfybetween"):
            yield Button("Back", variant="error", classes="w_m", id="cancelTransaction")
            yield Static()
            yield Static("", classes="error", id="msg")
            yield Static()
            yield Button("Submit", variant="primary", classes="w_m", id="addTransaction")
