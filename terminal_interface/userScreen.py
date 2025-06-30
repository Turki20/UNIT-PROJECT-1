from database.models import User
from datetime import datetime
from textual.screen import Screen
from textual.widgets import Static, DataTable, Input, Button, TextArea
from textual.containers import Container, ScrollableContainer
from database.db import execute, get_all
from textual import on

class ViewUsersScreen(Screen):
    BINDINGS = [
        ("b", "go_back", "Back to Home"),
        ("1", "add_user", "Add User"),
        ("2", "delete_user", "Delete User"),
        ("3", "update_user", "Update User"),
    ]

    def compose(self):
        with Container(id="header"):
            yield Static("Inventory Management System", id="Title")
            yield Static("User Management", id="pageTitle")
        
        with ScrollableContainer(classes="container users"):
            yield Static("User Table", classes="label")
            yield DataTable()

        with Container(classes="h"):
            with Container(classes="subcontainer"):
                yield Static("1. Add User")
                yield Static("2. Delete User")
                yield Static("3. Update User")

        with Container(classes="footer"):
            yield Static("Choose what you want by pressing the appropriate number.")
            yield Static("Press 'b' to go back", classes="label")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("ID", "Username", "Full Name", "Email", "Role", "Created At", "Updated At")
        users_data = get_all(User.get_all_users_query())
        users = User.convert_to_Users(users_data)
        table.add_rows([(u.id, u.username, u.full_name, u.email, u.role, u.created_at, u.updated_at) for u in users])

    def action_go_back(self):
        self.app.pop_screen()

    def action_add_user(self):
        self.app.push_screen(AddUserScreen())

    def action_delete_user(self):
        self.app.push_screen(DeleteUserScreen())

    def action_update_user(self):
        self.app.push_screen(UpdateUserScreen())

class AddUserScreen(Screen):

    @on(Button.Pressed, "#cancel")
    def back(self):
        self.app.pop_screen()

    @on(Button.Pressed, "#add")
    def add_user(self):
        msg = self.query_one("#msg")
        try:
            username = self.query_one("#username").value
            password = self.query_one("#password").value
            full_name = self.query_one("#fullname").value
            email = self.query_one("#email").value
            role = self.query_one("#role").value
            created_at = datetime.now().strftime("%d/%m/%Y")
            updated_at = created_at

            new_user = User(username, password, full_name, email, created_at, updated_at, role)
            execute(new_user.add_user_query())

            msg.set_class(True, "message")
            msg.set_class(False, "error")
            msg.update("User Added Successfully")

        except Exception as e:
            msg.set_class(True, "error")
            msg.set_class(False, "message")
            msg.update(f"{e}")

    def compose(self):
        with Container(id="header"):
            yield Static("Add New User", id="Title")

        with ScrollableContainer(classes="container"):
            yield Static("Username:", classes="label")
            yield Input(placeholder="Username", id="username")
            yield Static("Password:", classes="label")
            yield Input(placeholder="Password", id="password")
            yield Static("Full Name:", classes="label")
            yield Input(placeholder="Full Name", id="fullname")
            yield Static("Email:", classes="label")
            yield Input(placeholder="Email", id="email")
            yield Static("Role (Admin/InventoryStaff/ReadOnly):", classes="label")
            yield Input(placeholder="Role", id="role")

        with Container(classes="h justfybetween"):
            yield Button("Cancel", variant="error", id="cancel", classes="w_m")
            yield Static("", id="msg", classes="error")
            yield Button("Add", variant="success", id="add", classes="w_m")

class DeleteUserScreen(Screen):

    @on(Button.Pressed, "#back")
    def back(self):
        self.app.pop_screen()

    @on(Button.Pressed, "#delete")
    def delete_user(self):
        msg = self.query_one("#msg")
        try:
            user_id = int(self.query_one("#user_id").value)
            if len(get_all(User.get_user_by_id_query(user_id))) == 0:
                raise Exception("ID Not Exist!")
            execute(User.delete_user_query(user_id))
            msg.set_class(True, "message")
            msg.set_class(False, "error")
            msg.update("User deleted successfully.")

        except Exception as e:
            msg.set_class(True, "error")
            msg.set_class(False, "message")
            msg.update(str(e))

    def compose(self):
        with Container(id="header"):
            yield Static("Delete User", id="Title")

        with Container(classes="container center"):
            yield Static("Enter User ID to delete:", classes="label")
            yield Input(placeholder="User ID", id="user_id", type="integer")

            with Container(classes="h justfybetween"):
                yield Button("Back", id="back", variant="error", classes="w_m")
                yield Static("", id="msg", classes="error")
                yield Button("Delete", id="delete", variant="error", classes="w_m")

class UpdateUserScreen(Screen):

    @on(Button.Pressed, "#back")
    def back(self):
        self.app.pop_screen()

    @on(Button.Pressed, "#search")
    def search_user(self):
        msg = self.query_one("#msg")
        try:
            user_id = int(self.query_one("#user_id").value)
            user = get_all(User.get_user_by_id_query(user_id))
            if len(user) == 0:
                raise Exception("ID Not Exist!")

            user = user[0]
            self.query_one("#username").value = user[1]
            self.query_one("#password").value = user[2]
            self.query_one("#fullname").value = user[3]
            self.query_one("#email").value = user[4]
            self.query_one("#role").value = user[5]

        except Exception as e:
            msg.set_class(True, "error")
            msg.update(str(e))

    @on(Button.Pressed, "#update")
    def update_user(self):
        msg = self.query_one("#msg")
        try:
            user_id = int(self.query_one("#user_id").value)
            if len(get_all(User.get_user_by_id_query(user_id))) == 0:
                raise Exception("ID Not Exist!")

            username = self.query_one("#username").value
            password = self.query_one("#password").value
            full_name = self.query_one("#fullname").value
            email = self.query_one("#email").value
            role = self.query_one("#role").value
            updated_at = datetime.now().strftime("%d/%m/%Y")

            updated_user = User(username, password, full_name, email, "2025-01-01", updated_at, role, id=user_id)
            execute(updated_user.update_user_query())

            msg.set_class(True, "message")
            msg.set_class(False, "error")
            msg.update("User updated successfully.")

        except Exception as e:
            msg.set_class(True, "error")
            msg.set_class(False, "message")
            msg.update(str(e))

    def compose(self):
        with Container(id="header"):
            yield Static("Update User", id="Title")

        with Container(classes="container center"):
            yield Static("Enter User ID:", classes="label")
            yield Input(placeholder="User ID", id="user_id", type="integer")

            with Container(classes="h justfybetween"):
                yield Button("Back", id="back", variant="error", classes="w_m")
                yield Static("", id="msg", classes="error")
                yield Button("Search", id="search", variant="warning", classes="w_m")

        with ScrollableContainer(classes="container"):
            yield Static("Username:", classes="label")
            yield Input(id="username")
            yield Static("Password:", classes="label")
            yield Input(id="password")
            yield Static("Full Name:", classes="label")
            yield Input(id="fullname")
            yield Static("Email:", classes="label")
            yield Input(id="email")
            yield Static("Role (Admin/InventoryStaff/ReadOnly):", classes="label")
            yield Input(id="role")

            with Container(classes="h justfybetween"):
                yield Button("Update", id="update", variant="success", classes="w_m")

