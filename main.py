import datetime
import json
import os


# Класс для работы с задачами
class Task:
    def __init__(self, task_id, title, description,
                 category, due_date, priority, status):
        self.id = task_id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    # Метод для сохранения задачи в файл
    def save(self):
        if os.path.isfile('tasks.json'):
            with open('tasks.json', 'r') as f:
                tasks = json.load(f)
                tasks.append(self.__dict__)
                tasks = sorted(tasks, key=lambda x: x["id"])
            with open('tasks.json', 'w') as f:
                json.dump(tasks, f)
        else:
            with open('tasks.json', 'w') as f:
                tasks = [self.__dict__]
                json.dump(tasks, f)

    # Метод для загрузки задачи из файла
    @staticmethod
    def load(task_id):
        with open('tasks.json', 'r') as f:
            tasks = json.load(f)
        for task in tasks:
            if task["id"] == task_id:
                new_task = Task(
                    task["id"],
                    task["title"],
                    task["description"],
                    task["category"],
                    task["due_date"],
                    task["priority"],
                    task["status"])
                delete_task(task_id)
                return new_task

# Функция для просмотра списка задач


def view_tasks(category):
    flag = True
    tasks = load_tasks()
    if tasks != {}:
        for task in tasks:
            if category != "" and task["category"] == category:
                print(task["title"] + ":" + task["description"])
            elif category == "все":
                print(task["title"] + ":" + task["description"])
            else:
                flag = False
        if not flag:
            print("Такой категории нет в менеджере!")
    else:
        print("В менеджере задач пусто!")


# Функция для добавления новой задачи
def add_task():
    while True:
        title = input("Введите название задачи: ")
        if title == "":
            print("Необходимо ввести название задачи!")
            continue
        break

    while True:
        description = input("Введите описание задачи: ")
        if description == "":
            print("Описание задачи не может быть пустым!")
            continue
        break

    while True:
        category = input("Введите категорию задачи: ")
        if category == "":
            print("Категория задачи это обязательное поле!")
            continue
        break

    while True:
        due_date = input(
            "Введите срок выполнения задачи в формате ГГГГ-ММ-ДД: ")
        if due_date == "":
            print("Срок выполнения задачи не может быть пустым.")
            continue
        try:
            datetime.datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            print("Неправильный формат даты. Введите дату в формате ГГГГ-ММ-ДД.")
            continue
        break

    while True:
        priority = input("Введите приоритет задачи (низкий/средний/высокий): ")
        if priority not in ["низкий", "средний", "высокий"]:
            print(
                "Неправильный приоритет. Допустимые значения: низкий, средний, высокий.")
            continue
        break

    status = "не выполнена"

    if os.path.isfile('tasks.json'):
        with open('tasks.json', 'r') as f:
            tasks = json.load(f)
            task_id = tasks[-1]["id"] + 1
    else:
        task_id = 1

    task = Task(
        task_id,
        title,
        description,
        category,
        due_date,
        priority,
        status)
    task.save()


# Функция для изменения задачи
def edit_task(task_id):
    if os.path.isfile('tasks.json'):
        task = Task.load(task_id)
        field = input(
            "Введите поле, которое хотите изменить(если хотите отметить задачу как выполненную, введите выполнена): ")
        if field == "выполнена":
            task.__setattr__("status", "выполнена")
        elif field in ['title', 'description', 'category', 'due_date', 'priority']:
            value = input("Введите новое значение: ")
            task.__setattr__(field, value)
        else:
            print("Это поле не существует или его нельзя изменить!")
        task.save()
    else:
        print("В менеджере задач пусто!")


# Функция для удаления задачи по ид
def delete_task(task_id):
    tasks = load_tasks()
    if tasks != {}:
        for i in range(len(tasks)):
            if tasks[i]["id"] == int(task_id):
                del tasks[i]
                break
        with open('tasks.json', 'w') as f:
            json.dump(tasks, f)
    else:
        print("В менеджере задач пусто!")


# Функция для удаления задачи по категории
def delete_task_category(category):
    tasks = load_tasks()
    if tasks != {}:
        new_tasks = [i for i in tasks if category not in i["category"]]
        with open('tasks.json', 'w') as f:
            json.dump(new_tasks, f)
    else:
        print("В менеджере задач пусто!")


# Функция для поиска задачи
def search_tasks(keywords, category, status):
    tasks = load_tasks()
    if tasks != {}:
        results = []
        for task in tasks:
            if keywords != "":
                # Проверяем наличие ключевых слов в названии или описании
                # задачи
                if keywords.lower() in task["title"].lower(
                ) or keywords.lower() in task["description"].lower():
                    results.append(task)

            elif category != "":
                # Фильтруем по категории
                if task['category'] == category:
                    results.append(task)

            elif status != "":
                # Фильтруем по статусу
                if task['status'] == status:
                    results.append(task)

        for task in results:
            print(task["title"]+":"+task["description"])
            return results

        if not results:
            print("Ничего не найдено :(")
    else:
        print("В менеджере задач пусто!")


# Функция для загрузки задач из файла
def load_tasks():
    if os.path.isfile('tasks.json'):
        with open('tasks.json', 'r') as f:
            tasks = json.load(f)
    else:
        tasks = {}
    return tasks


# Главный цикл программы
def main():
    print("✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿")
    print("    ДОБРО ПОЖАЛОВАТЬ В МЕНЕДЖЕР ЗАДАЧ  ")
    print("✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿")
    print("Возможные команды менеджера задач:\n☆ просмотр\n☆ добавление\n☆ изменение\n☆ удаление\n☆ поиск\n☆ выход")
    while True:
        command = input("Введите команду ☞ ")
        if command == "просмотр":
            category = input(
                "Введите категорию (для просмотра всех задач, введите \"все\"): ")
            view_tasks(category)
        elif command == "добавление":
            add_task()
        elif command == "изменение":
            task_id = int(input("Введите ID задачи: "))
            edit_task(task_id)
        elif command == "удаление":
            task_id = input(
                "Введите ID задачи для удаления (нажмите ENTER если хотите удалить задачу по категории): ")
            if task_id == "":
                category = input("Введите категорию: ")
                delete_task_category(category)
            else:
                delete_task(task_id)
        elif command == "поиск":
            keywords = input(
                "Введите ключевое слово для поиска (нажмите ENTER, если хотите выполнить поиск по категории): ")
            if keywords != "":
                search_tasks(keywords, "", "")
            else:
                category = input(
                    "Введите категорию для поиска (нажмите ENTER, если хотите выполнить поиск по статусу): ")
                if category != "":
                    search_tasks("", category, "")
                else:
                    status = input(
                        "Введите статус выполнения команды для поиска: ")
                    search_tasks("", "", status)
        elif command == "выход":
            break
        else:
            print("Такой команды нет в менеджере задач!")


if __name__ == "__main__":
    main()
