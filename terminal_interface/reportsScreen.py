from textual.screen import Screen
from textual.widgets import Static, DataTable, Input, Button
from textual.containers import ScrollableContainer, Container
from database.db import get_all, execute
from database.models import Report
from textual import on


class ViewReportsScreen(Screen):
    BINDINGS = [
        ("b", "go_back", "Back to Home"),
        ("1", "delete_report", "Delete report"),
    ]

    def compose(self):
        with Container(id="header"):
            yield Static("Inventory Management System", id="Title")
            yield Static("Reports Management", id="pageTitle")

        with ScrollableContainer(classes="container products"):
            yield Static("Reports Table", classes="label")
            yield DataTable()

        with Container(classes="h"):
            with Container(classes="subcontainer"):
                yield Static("1. Delete a Report")

        with Container(classes="footer"):
            yield Static("Choose what you want by pressing the appropriate number.")
            yield Static("Press 'b' to go back", classes="label")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("id", "type", "content", "created_at", "created_by")

        all_reports = get_all(Report.get_all_reports_query())
        reports = Report.convert_to_Reports(all_reports)

        new_list = []
        for report in reports:
            new_list.append((
                report.report_id,
                report.report_type,
                report.content[:50] + "..." if len(report.content) > 50 else report.content,
                report.created_at,
                report.created_by if report.created_by is not None else "System"
            ))

        table.add_rows(new_list)

    def action_go_back(self):
        self.app.pop_screen()

    def action_delete_report(self):
        self.app.push_screen(DeleteReport())


class DeleteReport(Screen):
    msg_status = False

    @on(Button.Pressed, "#Delete")
    def delete_report(self):
        if not DeleteReport.msg_status:
            msg = self.query_one("#msg")
            msg.set_class(False, "hide")
            msg.set_class(True, "block")
            DeleteReport.msg_status = True
        else:
            msg = self.query_one("#msg")
            msg.set_class(True, "hide")
            msg.set_class(False, "block")
            DeleteReport.msg_status = False

    @on(Button.Pressed, "#back")
    def back_to_reports_screen(self):
        self.app.pop_screen()

    @on(Button.Pressed, "#yes")
    def delete(self):
        report_id = self.query_one("#report_id").value
        try:
            report_id = int(report_id)
            if len(get_all(Report.get_report_by_id_query(report_id))) == 0:
                raise Exception("ID Not Exist!.")
            execute(Report.delete_report_query(report_id))
            self.app.pop_screen()

        except Exception as e:
            msg = self.query_one("#feedback")
            msg.update(f"{e}")
            msg = self.query_one("#msg")
            msg.set_class(True, "hide")
            msg.set_class(False, "block")
            DeleteReport.msg_status = False

    def compose(self):
        with Container(classes="container center"):
            yield Static("Enter the Report ID", classes="label")
            yield Input(placeholder="ID", id="report_id", type="integer")

            with Container(classes="h justfybetween"):
                yield Button("Back", classes="w_m", id="back")
                yield Static()
                yield Static(id="feedback", classes="error")
                yield Static()
                yield Button("Delete", id="Delete", variant="error", classes="w_m")

            with Container(classes="warning hide", id="msg"):
                yield Static("Are you sure you want to delete?")
                yield Button("Yes", variant="error", id="yes")
