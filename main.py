from textual.app import App, ComposeResult
from textual.widgets import  Label, Button ,Static
from textual.containers import Container
from textual.screen import Screen
from datetime import datetime

class Task(Static):
    def __init__(self,task_id:str,name:str,task_time:str,completed:bool,repeatable:bool,deadline:datetime = None,*args,**kwargs):
            super().__init__(*args,**kwargs)
            self.task_name = name
            self.task_time = task_time
            self.repeatable= repeatable
            self.deadline= deadline
            self.completed = completed
            self.task_id = task_id 

    def compose(self)-> ComposeResult:
        deadline_str = f"[bold purple]Deadline:{self.deadline.strftime('%Y-%m-%d %H:%M')}[/]" if self.deadline else "[bold light blue]No Deadline[/]"
        repeat_str = "[bold dim yellow]Repeatable[/]" if self.repeatable else "[bold orange]Not Repeatable[/]"
        complete_str = "[bold green]Completed[/]" if self.completed else "[bold red]Not Completed[/]"
        yield Label (f"----{self.task_id}----",classes="task-detail")
        yield Label(f"[b]Task :[/b]{self.task_name}",classes="task-detail")
        yield Label(f"[b]Time :[/b]{self.task_time}",classes="task-detail")
        yield Label(f"[b]Status :[/b]{complete_str}",classes="task-detail")
        yield Label(f"{repeat_str}",classes="task-detail")
        yield Label(f"{deadline_str}",classes="task-detail")
        

class CustomTimer(Static):
    def on_mount(self) -> None:
        """Called when the widget is added to the DOM."""
        self.set_interval(5, self.update_time)
        self.update_time()

    def update_time(self) -> None:
        """Method to get the current time and update the Label."""
        current_datetime = datetime.now()
        formatted_time = current_datetime.strftime("%H:%M:%S")
        self.query_one("#current-time-label", Label).update(formatted_time)

    def compose(self) -> ComposeResult:
        yield Label("", id="current-time-label")

class Activecont(Static):
    def compose(self)->ComposeResult:
        yield CustomTimer()

class TaskListCont(Static):
    def compose(self)->ComposeResult:
        yield Label("[bold white on $primary]My Tasks[/]",classes = "title")
        yield Task(
            task_id ="1",
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
