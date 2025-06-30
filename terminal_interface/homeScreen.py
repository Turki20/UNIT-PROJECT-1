
from textual.screen import Screen
from textual.widgets import Static, Rule, DataTable, Input, Button
from textual.containers import Container, ScrollableContainer
from terminal_interface.productScreen import ViewProductsScreen

class HomePage(Screen):
    
    BINDINGS = [("3", "product_page", "Go to View Products")]

    def compose(self):
        with Container(id="header"):
            yield Static("Inventory Management System", id="Title")
            yield Static("Home Page", id="pageTitle")
        
        with Container(classes="container"):
            yield Static("1. Record a Sale", classes="label")
            yield Static("2. Record a Purchase", classes="label")
            yield Static("3. Product Management", classes="label")
            yield Static("4. Reports", classes="label")
            yield Static("5. Alerts", classes="label")
            yield Static("6. Manage Users", classes="label")
            yield Static("7. Warehouse Settings", classes="label")

            with Container(classes="footer"):
                yield Static("Choose what you want by pressing the appropriate number on the keyboard.")
        
    def action_product_page(self):
        self.app.push_screen(ViewProductsScreen())
