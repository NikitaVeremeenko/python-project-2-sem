from enum import Enum
from datetime import date
from uuid import UUID, uuid4


class PriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task:
    def __init__(self, title, priority, due_date):
        self.id = str(uuid4())
        self.title = title
        self.priority = priority
        self.due_date = due_date
        self.completed = False


class ToDoList:
    def __init__(self):
        self.tasks = []

    def create_task(self, title, priority, due_date):
        task = Task(title, priority, due_date)
        self.tasks.append(task)
        print("Задача успешно создана.")

    def update_task(self, task_id, title=None, priority=None, due_date=None):
        task = self._get_task_by_id(task_id)
        if not task:
            print("Задача не найдена.")
            return

        if title is not None:
            task.title = title
        if priority is not None:
            task.priority = priority
        if due_date is not None:
            task.due_date = due_date

        print("Задача успешно обновлена.")

    def delete_task(self, task_id):
        task = self._get_task_by_id(task_id)
        if not task:
            print("Задача не найдена.")
            return

        self.tasks.remove(task)
        print("Задача успешно удалена.")

    def complete_task(self, task_id):
        task = self._get_task_by_id(task_id)
        if not task:
            print("Задача не найдена.")
            return

        task.completed = True
        print("Задача отмечена как выполненная.")

    def sort_tasks(self, sort_by):
        valid_sort_fields = ["priority", "due_date"]
        if sort_by not in valid_sort_fields:
            print(f"Некорректное поле сортировки. Доступные поля: {', '.join(valid_sort_fields)}")
            return

        sorted_tasks = sorted(self.tasks, key=lambda x: getattr(x, sort_by))
        self.tasks = sorted_tasks

    def show_tasks(self):
        for task in self.tasks:
            print(f"ID: {task.id}")
            print(f"Название: {task.title}")
            print(f"Приоритет: {task.priority}")
            print(f"Дата выполнения: {task.due_date}")
            print(f"Статус: {'Выполнено' if task.completed else 'Не выполнено'}")
            print("------------------------")

    def _get_task_by_id(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None


def main():
    todo_list = ToDoList()

    while True:
        print("Меню:")
        print("1. Создать задачу")
        print("2. Обновить задачу")
        print("3. Удалить задачу")
        print("4. Отметить задачу как выполненную")
        print("5. Сортировать задачи")
        print("6. Показать задачи")
        print("0. Выйти")

        choice = input("Введите номер операции: ")

        if choice == "1":
            title = input("Введите название задачи: ")
            priority = input("Введите приоритет задачи (low, medium, high): ")
            due_date = input("Введите дату выполнения задачи (ГГГГ-ММ-ДД): ")
            try:
                due_date = date.fromisoformat(due_date)
            except ValueError:
                print("Некорректная дата.")
                continue

            if priority not in PriorityEnum.__members__.values():
                print("Некорректный приоритет.")
                continue

            todo_list.create_task(title, priority, due_date)
        elif choice == "2":
            task_id = input("Введите ID задачи для обновления: ")
            title = input("Введите новое название задачи (оставьте пустым, чтобы не менять): ")
            priority = input("Введите новый приоритет задачи (оставьте пустым, чтобы не менять): ")
            due_date = input("Введите новую дату выполнения задачи (ГГГГ-ММ-ДД, оставьте пустым, чтобы не менять): ")
            try:
                due_date = date.fromisoformat(due_date) if due_date else None
            except ValueError:
                print("Некорректная дата.")
                continue

            if priority and priority not in PriorityEnum.__members__.values():
                print("Некорректный приоритет.")
                continue

            todo_list.update_task(task_id, title, priority, due_date)
        elif choice == "3":
            task_id = input("Введите ID задачи для удаления: ")
            todo_list.delete_task(task_id)
        elif choice == "4":
            task_id = input("Введите ID задачи для отметки как выполненной: ")
            todo_list.complete_task(task_id)
        elif choice == "5":
            sort_by = input("Введите поле сортировки (priority, due_date): ")
            todo_list.sort_tasks(sort_by)
        elif choice == "6":
            todo_list.show_tasks()
        elif choice == "0":
            print("Программа завершена.")
            break
        else:
            print("Некорректный выбор операции.")


if __name__ == "__main__":
    main()
