# logic.py
import xml.etree.ElementTree as ET
import uuid
import os # To check if the file exists for initial creation

TASKS_FILE = "tasks.xml"

# Internal helper function to load tasks from XML
def _load_tasks_xml():
    tasks = []
    if not os.path.exists(TASKS_FILE):
        # If the file doesn't exist, return an empty list and create an empty XML structure
        _save_tasks_xml([])
        return []

    try:
        tree = ET.parse(TASKS_FILE)
        root = tree.getroot()
        for element in root.findall("task"):
            task_id = element.get('task_id')
            task_name = element.get('task_name')
            task_time = element.get('task_time')
            deadline = element.get('deadline')
            completed = element.get('completed') == 'true' # Convert string "true"/"false" to boolean
            repeatable = element.get('repeatable') == 'true' # Convert string "true"/"false" to boolean

            tasks.append({
                'task_id': task_id,
                'task_name': task_name,
                'task_time': task_time,
                'deadline': deadline,
                'completed': completed,
                'repeatable': repeatable
            })
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}. Creating a new empty task list.")
        _save_tasks_xml([]) # Re-initialize with an empty list if parsing fails
        return []
    except FileNotFoundError:
        # This case should be handled by os.path.exists, but kept for robustness
        pass
    return tasks

# Internal helper function to save tasks to XML
def _save_tasks_xml(task_data: list[dict]):
    root = ET.Element("tasks")
    for task_dict in task_data:
        task_element = ET.SubElement(root, "task")
        # Set attributes from the dictionary
        task_element.set('task_id', task_dict.get('task_id', str(uuid.uuid4()))) # Ensure ID
        task_element.set('task_name', task_dict.get('task_name', ''))
        task_element.set('task_time', task_dict.get('task_time', '0')) # Default time to 0
        task_element.set('deadline', task_dict.get('deadline', ''))
        task_element.set('completed', str(task_dict.get('completed', False)).lower()) # Convert boolean to "true"/"false"
        task_element.set('repeatable', str(task_dict.get('repeatable', False)).lower()) # Convert boolean to "true"/"false"

    tree = ET.ElementTree(root)
    tree.write(TASKS_FILE, encoding="utf-8", xml_declaration=True)

# Initialize tasks when the module is loaded
_current_tasks = _load_tasks_xml()

# --- Public API for Task Management ---

def get_tasks(include_completed: bool = False) -> list[dict]:
    """
    Returns a list of task dictionaries.
    If include_completed is False, only uncompleted tasks are returned.
    """
    if include_completed:
        return list(_current_tasks) # Return a copy to prevent external modification
    else:
        return [task for task in _current_tasks if not task['completed']]

def add_task(task_name: str, task_time: str = "25", deadline: str = "", repeatable: bool = False) -> str:
    """
    Adds a new task and returns its ID.
    task_time is in minutes (e.g., "25" for 25 minutes).
    """
    new_task_id = str(uuid.uuid4())
    new_task = {
        'task_id': new_task_id,
        'task_name': task_name,
        'task_time': task_time,
        'deadline': deadline,
        'completed': False,
        'repeatable': repeatable
    }
    _current_tasks.append(new_task)
    _save_tasks_xml(_current_tasks)
    return new_task_id

def update_task(task_id: str, **kwargs) -> bool:
    """
    Updates attributes of an existing task.
    e.g., update_task(task_id, completed=True, task_time="30")
    """
    for i, task in enumerate(_current_tasks):
        if task['task_id'] == task_id:
            for key, value in kwargs.items():
                if key in task: # Only update valid keys
                    # Special handling for boolean fields
                    if key in ['completed', 'repeatable'] and isinstance(value, str):
                        task[key] = value.lower() == 'true'
                    else:
                        task[key] = value
            _current_tasks[i] = task # Update the task in the list
            _save_tasks_xml(_current_tasks)
            return True
    return False

def complete_task(task_id: str) -> bool:
    """Marks a task as completed."""
    return update_task(task_id, completed=True)

def uncomplete_task(task_id: str) -> bool:
    """Marks a task as uncompleted."""
    return update_task(task_id, completed=False)

def delete_task(task_id: str) -> bool:
    """Deletes a task."""
    global _current_tasks
    initial_count = len(_current_tasks)
    _current_tasks = [task for task in _current_tasks if task['task_id'] != task_id]
    if len(_current_tasks) < initial_count:
        _save_tasks_xml(_current_tasks)
        return True
    return False

# Example Usage (for testing)
if __name__ == "__main__":
    print("--- Initial Tasks ---")
    print(get_tasks(include_completed=True))

    print("\n--- Adding a task ---")
    new_id1 = add_task("Learn Textualize Widgets", "30", "2025-08-01")
    print(get_tasks())

    print("\n--- Adding another task ---")
    new_id2 = add_task("Plan next project", "60", "2025-07-20", repeatable=True)
    print(get_tasks())

    print(f"\n--- Completing task: {new_id1} ---")
    complete_task(new_id1)
    print("Uncompleted tasks:")
    print(get_tasks())
    print("All tasks:")
    print(get_tasks(include_completed=True))

    print(f"\n--- Updating task time for {new_id2} ---")
    update_task(new_id2, task_time="45")
    print(get_tasks(include_completed=True))

    print(f"\n--- Deleting task: {new_id1} ---")
    delete_task(new_id1)
    print(get_tasks(include_completed=True))

    print("\n--- Adding a task without specific time/deadline ---")
    add_task("Buy groceries")
    print(get_tasks(include_completed=True))

    # Clean up for fresh start next time you run it
    # import os
    # if os.path.exists(TASKS_FILE):
    #     os.remove(TASKS_FILE)
    # print(f"\nRemoved {TASKS_FILE} for a fresh start.")
