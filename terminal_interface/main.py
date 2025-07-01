from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Rule, DataTable, Input
from textual.containers import ScrollableContainer, Container
from textual.screen import Screen
from textual import on

from terminal_interface.homeScreen import HomePage
from database.models import User
from user import auth
from user.session import Session


Session.current_user = None


class LoginPage(Screen):
    
    @on(Button.Pressed, "#submit_login")
    def check_username_password(self):
        username = self.query_one("#username", Input).value
        password = self.query_one("#password", Input).value
        msg = self.query_one("#massege", Static)
        check_user = auth.check_user_exist(username, password)
        if check_user != None:
            Session.current_user = check_user
            self.app.push_screen(HomePage())
        else:
            msg.update("user name or password was wrong, please try again.")
    
    def compose(self):
        Session.current_user = None
        with Container(id="header"):
            yield Static("Inventory Management System", id="Title")
            yield Static("Login Page", id="pageTitle")
            
        with Container(classes="container"):
            yield Static("", classes="error", id="massege")
            yield Static("User Name: ", classes="label")
            yield Input(placeholder="Enter your username", id="username")
            yield Static("Password: ", classes="label")
            yield Input(placeholder="Enter your password", id="password")
            with Container(id="container"):
                yield Button("Submit", id="submit_login", variant="success", classes="btn")

class InventoryApp(App):
    
    CSS_PATH = "style.css"

    def on_mount(self):
        if Session.current_user == None:
            self.install_screen(LoginPage(), "loginScreen")
            self.push_screen("loginScreen")
            #self.push_screen(HomePage())


if __name__ == "__main__":
    InventoryApp().run()
