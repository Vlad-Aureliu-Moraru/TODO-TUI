from textual.app import App, ComposeResult
from textual.logging import TextualHandler
import logging
from textual.widgets import Label, Button, Static
from textual.containers import Container
from textual.screen import Screen
from ui import MainScreen  # Assuming ui.py defines a MainScreen
import logic as lo

logging.basicConfig(
    level="NOTSET",
    handlers=[TextualHandler()],
)


class MyApp(App):
    CSS_PATH = "main.tcss"

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit_app", "Quit"),
        ("a", "add_task_prompt", "Add Task"),
    ]

    def on_mount(self) -> None:
        self.push_screen(MainScreen())
        
        try:
            main_screen_instance = self.query_one(MainScreen)
            tasks_data = lo.get_tasks(include_completed=True)
            logging.debug(f"Tasks from get_tasks: {tasks_data}")
            main_screen_instance.update_task_list_ui(tasks_data)
            logging.debug(f"Tasks loaded and updated UI: {tasks_data}")
        except Exception as e:
            self.log.error(f"Failed to update task list: {e}")

    def action_toggle_dark(self) -> None:
        self.bell()
    def action_quit_app(self) -> None:
        self.exit("Exiting application.")

    def action_add_task_prompt(self) -> None:
        """Prompt the user for a new task and add it."""
        self.bell()  
        new_task_description = self.query_one(MainScreen).prompt_for_task()  # Placeholder; implement in MainScreen

        if new_task_description:
            task_id = lo.add_task(task_name=new_task_description)
            self.notify(f"Task '{new_task_description}' added! ID: {task_id}")
            try:
                main_screen_instance = self.query_one(MainScreen)
                tasks_data = lo.get_tasks(include_completed=False)
                main_screen_instance.update_task_list_ui(tasks_data)
            except Exception as e:
                self.log.error(f"Failed to refresh task list: {e}")
        else:
            self.notify("Task addition cancelled.", severity="warning")

if __name__ == "__main__":
    app = MyApp()
    app.run()  
