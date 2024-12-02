from unittest.mock import patch
import pytest
from main import *

# Тесты для проверки функций добавления, выполнения, поиска и удаления задач


@pytest.fixture(autouse=True)
def clear_tasks_json_file():
    # Очищаем файл tasks.json перед каждым тестом
    if os.path.exists('tasks.json'):
        os.remove('tasks.json')


# Функция для создания экземпляра класса Задач
def create_test_task():
    task = Task(
        1,
        "Тестовая задача",
        "Описание задачи",
        "Работа",
        "2024-12-31",
        "высокий",
        "не выполнена"
    )
    task.save()


@patch('builtins.input', side_effect=['Тестовая задача',
       'Описание', 'Работа', '2024-12-31', 'высокий'])
def test_add_task(self):
    add_task()
    with open('tasks.json', 'r') as f:
        data = json.load(f)
    task = data[0]
    assert task['title'] == 'Тестовая задача'
    assert task['description'] == 'Описание'
    assert task['category'] == 'Работа'
    assert task['due_date'] == '2024-12-31'
    assert task['priority'] == 'высокий'
    assert task['status'] == 'не выполнена'


@patch('builtins.input', side_effect=['выполнена'])
def test_edit_complete_task(self):
    create_test_task()
    edit_task(1)

    with open('tasks.json', 'r') as f:
        data = json.load(f)
    task = data[0]
    assert task['status'] == 'выполнена'


def test_search_tasks():
    create_test_task()
    results = search_tasks("", "Работа", "")
    assert results[0]['title'] == 'Тестовая задача'


def test_delete_task():
    create_test_task()
    delete_task(1)
    tasks = load_tasks()
    assert tasks == []
