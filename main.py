from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, Button ,Static
from textual.containers import Container
from textual.screen import Screen
from datetime import datetime

class Task(Static):
    def __init__(self,name:str,task_time:str,completed:bool,repeatable:bool,deadline:datetime = None,*args,**kwargs):
            super().__init__(*args,**kwargs)
            self.task_name = name
            self.task_time = task_time
            self.repeatable= repeatable
            self.deadline= deadline
            self.completed = completed

    def compose(self)-> ComposeResult:
        deadline_str = f"[bold purple]Deadline:{self.deadline.strftime('%Y-%m-%d %H:%M')}[/]" if self.deadline else "[bold light blue]No Deadline[/]"
        repeat_str = "[bold dim yellow]Repeatable[/]" if self.repeatable else "[bold orange]Not Repeatable[/]"
        complete_str = "[bold green]Completed[/]" if self.completed else "[bold red]Not Completed[/]"
        yield Label(f"[b]Task :[/b]{self.task_name}",classes="task-detail")
        yield Label(f"[b]Time :[/b]{self.task_time}",classes="task-detail")
        yield Label(f"[b]Status :[/b]{complete_str}",classes="task-detail")
        yield Label(f"{repeat_str}",classes="task-detail")
        yield Label(f"{deadline_str}",classes="task-detail")



class CustomHeader(Static):
    def compose(self)->ComposeResult:
        yield Button("Create New Task",id="create_task_btn",compact=True,variant="default",classes="action-btn")
    def on_button_pressed(self,event:Button.Pressed)->None:
        if event.button.id == "create_task_btn":
            self.app.bell()

class Activecont(Static):
    def compose(self)->ComposeResult:
        yield Label("ACTIVE")
        yield CustomHeader()

class TaskListCont(Static):
    def compose(self)->ComposeResult:
        yield Label("[bold white on $primary]My Tasks[/]",classes = "title")
        yield Task(
            name="Learn",
            task_time="2 hours",
            completed= False,
            repeatable= False,
            deadline=datetime(2025,7,15,10,0)

        )



class MainScreen(Screen):
    def compose(self) -> ComposeResult:
        with Container(classes = "main-cont"):
            yield Activecont() 
            yield TaskListCont() 
        


# Define the main application class
class MyApp(App):

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit_app", "Quit"),
    ]
    CSS_PATH = "main.tcss"
    def on_mount(self) -> None:
        """Called when app is mounted."""
        self.push_screen(MainScreen()) # Push our main screen onto the app's stack

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_quit_app(self) -> None:
        """An action to quit the application."""
        self.exit("Exiting application.") # Exit gracefully

if __name__ == "__main__":
    app = MyApp()
    app.run()
