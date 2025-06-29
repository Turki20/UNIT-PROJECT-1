from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Rule, DataTable, Input
from textual.containers import ScrollableContainer, Container
from textual.screen import Screen

from database.models import User
user = None

# 🟩 الصفحة الرئيسية
class HomePageScreen(Screen):
    BINDINGS = [("1", "go_view", "Go to View Products")]

    def compose(self) -> ComposeResult:
        yield Static("Main Menu", id="Title")
        yield Rule(line_style="heavy")
        yield Static("1. View All Products", classes="label")
        yield Static("2. Add Product", classes="label")
        yield Static("3. Delete Product", classes="label")
        yield Static("4. Update Product", classes="label")

    def action_go_view(self):
        # الانتقال إلى شاشة عرض المنتجات
        self.app.push_screen(ViewProductsScreen())

ROWS = [
    ("lane", "swimmer", "country", "time"),
    (4, "Joseph Schooling", "Singapore", 50.39),
    (2, "Michael Phelps", "United States", 51.14),
    (5, "Chad le Clos", "South Africa", 51.14),
    (6, "László Cseh", "Hungary", 51.14),
    (3, "Li Zhuhao", "China", 51.26),
    (8, "Mehdy Metella", "France", 51.58),
    (7, "Tom Shields", "United States", 51.73),
    (1, "Aleksandr Sadovnikov", "Russia", 51.84),
    (10, "Darren Burns", "Scotland", 51.84),
]

    
# 🟦 شاشة عرض المنتجات
class ViewProductsScreen(Screen):
    BINDINGS = [("b", "go_back", "Back to Home")]

    def compose(self) -> ComposeResult:
        yield Static("Product List", id="Title")
        yield Rule()
        yield DataTable()
        yield Static("Press 'b' to go back", classes="label")
        yield Input(placeholder="First Name")
        yield Button("Btn", variant="success")
        yield Button("Btn", variant="error")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*ROWS[0])
        table.add_rows(ROWS[1:])
        
    def action_go_back(self):
        self.app.pop_screen()

class LoginPage(Screen):
    
    def compose(self):
        yield Static("Login", id="Title")
        yield Rule()
        yield Static("User Name: ", classes="label")
        yield Input(placeholder="Enter your username")
        yield Static("Password: ", classes="label")
        yield Input(placeholder="Enter your password")
        with Container(id="container"):
            yield Button("Submit", id="btn", variant="success")

class InventoryApp(App):
    
    CSS_PATH = "style.css"

    def on_mount(self):
        user = None
        self.push_screen(LoginPage())


if __name__ == "__main__":
    InventoryApp().run()
