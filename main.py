# main.py
from textual.app import App, ComposeResult
from textual.widgets import Label, Button, Static
from textual.containers import Container
from textual.screen import Screen # Screen is generally used for pushing/popping different views

from ui import MainScreen  # Assuming ui.py defines a MainScreen
import logic as lo

# Your `update_task_list` logic should ideally be a method within your App
# or passed to the screen that needs to update its widgets.
# Let's integrate it into the App's on_mount.

class MyApp(App):
    # Set the initial CSS path
    CSS_PATH = "main.tcss"

    # Define application-wide key bindings
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit_app", "Quit"),
        ("a", "add_task_prompt", "Add Task"), # New binding for adding tasks
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        # MainScreen should be the primary content of your app
        yield MainScreen()

    def on_mount(self) -> None:
        """Called when app is mounted."""
        # Get the instance of your MainScreen to update its contents
        main_screen_instance = self.query_one(MainScreen)

        # Load tasks using your logic module's public API
        tasks_data = lo.get_tasks(include_completed=False) # Get uncompleted tasks by default
       # main_screen_instance.update_task_list_ui(tasks_data)
        self.log(f"Tasks loaded and updated UI: {tasks_data}") # Use self.log for debugging

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark # Textual's built-in dark mode toggle
        self.log(f"Dark mode toggled: {self.dark}")

    def action_quit_app(self) -> None:
        """An action to quit the application."""
        self.exit("Exiting application.") # Exit gracefully

    def action_add_task_prompt(self) -> None:
        """Action to prompt the user for a new task and add it."""
        self.app.bell() # Play a sound to indicate interaction
        new_task_description = self.app.prompt("Enter new task description:")

        if new_task_description:
            # Use your logic module to add the task
            task_id = lo.add_task(task_name=new_task_description)
            self.notify(f"Task '{new_task_description}' added! ID: {task_id}")

            # After adding, refresh the task list in the UI
            main_screen_instance = self.query_one(MainScreen)
            tasks_data = lo.get_tasks(include_completed=False)
#            main_screen_instance.update_task_list_ui(tasks_data)
        else:
            self.notify("Task addition cancelled.", severity="warning")


if __name__ == "__main__":
    app = MyApp()
    app.run()
