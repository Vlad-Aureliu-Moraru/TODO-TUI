import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid
import io 

@dataclass
class Task_model:
    task_id :str
    task_name:str
    task_time: int
    task_repeatable:bool
    task_deadline:Optional[datetime] = None
    completed:bool = False



def get_tasks_from_xml():
    tree =  ET.parse("tasks.xml")
    root = tree.getroot()
    print(root)
    print(root[0].attrib)



def write_task_into_xml(task_model_instance:Task_model):
    task_name = task_model_instance.task_name
    task_id = task_model_instance.task_id
    task_repeatable = str(task_model_instance.task_repeatable).lower()
    task_completed =str(task_model_instance.completed).lower()
    task_time = str(task_model_instance.task_time)
    if task_model_instance.task_deadline is None:
        task_deadline = ""
    else:
        task_deadline= task_model_instance.task_deadline.strftime('%Y-%m-%d %H:%M')
    tree = None
    data = None
    try:
        tree = ET.parse("tasks.xml")
        data =tree.getroot()
        print("task file found and parsed SUCCESFULLY")
    except FileNotFoundError:
        data = ET.Element('tasks')
        tree = ET.ElementTree(data)
        print("task file NOT found and created SUCCESFULLY")
    except ET.ParseError:
        print("Warning parsing incorectly")
        data = ET.Element('tasks')
        tree = ET.ElementTree(data)
    task = ET.SubElement(data,'task')
    task.set('task_name',task_name)
    task.set('task_id',task_id)
    task.set('task_repeatable',task_repeatable)
    task.set('task_completed',task_completed)
    task.set('task_time',task_time)
    task.set('task_deadline',task_deadline)
    ET.indent(tree,space=" ")
    tree.write("tasks.xml",encoding="utf-8",xml_declaration=True)


if __name__ == "__main__":
    my_first_task = Task_model(task_deadline=None,task_id=str(uuid.uuid4()),task_name="test",task_repeatable=False,task_time=20)
#    print(my_first_task)
#   write_task_into_xml(my_first_task)
    get_tasks_from_xml()
