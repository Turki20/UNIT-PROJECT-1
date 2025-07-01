
from textual.screen import Screen
from textual.widgets import Static, Rule, DataTable, Input, Button
from textual.containers import Container, ScrollableContainer
from terminal_interface.productScreen import ViewProductsScreen
from terminal_interface.salesPurchaseScreen import AddTransaction
from terminal_interface.userScreen import ViewUsersScreen
from user.session import Session

class HomePage(Screen):
    
    BINDINGS = [
        ("1", "transactio_page", "Go to Transaction"),
        ("2", "product_page", "Go to View Products"),
        ("5", "manage_users", "Go to View Users"),
        ("7", "logout", "Go to login"),
    ]

    def compose(self):
        with Container(id="header"):
            yield Static("Inventory Management System", id="Title")
            yield Static("Home Page", id="pageTitle")
        
        with Container(classes="container"):
            yield Static("1. Register a purchase or sale transaction", classes="label")
            yield Static("2. Product Management", classes="label")
            yield Static("3. Reports", classes="label")
            yield Static("4. Alerts", classes="label")
            yield Static("5. Manage Users", classes="label")
            yield Static("6. Warehouse Settings", classes="label")
            yield Static("7. Logout", classes="label")

            with Container(classes="footer"):
                yield Static("Choose what you want by pressing the appropriate number on the keyboard.")
        
    def action_product_page(self):
        self.app.push_screen(ViewProductsScreen())
    
    def action_transactio_page(self):
        self.app.push_screen(AddTransaction())
    
    def action_manage_users(self):
        self.app.push_screen(ViewUsersScreen())
        
    def action_logout(self):
        Session.current_user = None
        # self.app.push_screen(LoginPage())
        self.app.pop_screen()
