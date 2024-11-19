from task_utils import (load_json_data, build_station_dict, build_graph,
                        remove_unconnected_nodes, build_labels_dict, find_station_id,
                        Task, assign_initial_tasks, assign_remaining_tasks,)

from datetime import timedelta, time
from operator import itemgetter

def main():
    # Загрузка данных для графа
    names = load_json_data("l10n.json")
    graph_data = load_json_data("data.json")

    # Построение графа и словарей
    node_station_dict = build_station_dict(graph_data['stops']['items'])
    global G, labels  # Делаем G и labels доступными в assign_tasks_to_employees
    G = build_graph(graph_data['nodes']['items'], graph_data['links']['items'])
    G = remove_unconnected_nodes(G)
    labels = build_labels_dict(names, node_station_dict)

    # Пример списка задач
    tasks_list = [["Ботанический сад", "Рижская", 9, 30], ["ВДНХ", "Проспект мира", 10, 45], ["Охотный ряд", "Театральная", 11, 15], ["Новокосино", "Шоссе Энтузиастов", 12, 0], ["Киевская", "Арбатская", 13, 20], ["Беговая", "Улица 1905 года", 14, 50], ["Речной вокзал", "Войковская", 15, 10], ["Южная", "Чертановская", 16, 30], ["Таганская", "Китай-город", 17, 5], ["Перово", "Новогиреево", 17, 45], ["Щёлковская", "Первомайская", 18, 15], ["Третьяковская", "Парк Культуры", 19, 0], ["Бабушкинская", "Свиблово", 20, 25], ["Лубянка", "Чистые пруды", 21, 40], ["Каширская", "Коломенская", 22, 30], ["Бабушкинская", "Таганская", 8, 45], ["Тропарёво", "Славянский бульвар", 9, 20], ["Юго-Западная", "Киевская", 10, 0], ["Площадь Ильича", "Каширская", 11, 30], ["Щукинская", "Парк Победы", 12, 15], ["Полежаевская", "Октябрьская", 13, 45]]

    # Сортировка заявок по времени начала
    tasks_list = sorted(tasks_list, key=itemgetter(2, 3))

    # Инициализация задач с проверкой наличия станций
    task_objects = []
    for t in tasks_list:
        st1_id = find_station_id(labels, t[0])
        st2_id = find_station_id(labels, t[1])

        if st1_id is None or st2_id is None:
            print(f"Предупреждение: Одна или обе станции '{t[0]}' или '{t[1]}' не найдены в графе. Заявка пропущена.")
            continue  # Пропустить задание, если одна из станций не найдена

        # Добавляем задачу только если станции найдены
        task_objects.append(Task(t[0], t[1], time(t[2], t[3]), G, labels))

    # Количество сотрудников
    num_employees = 3
    employees = [{'id': i + 1, 'available_time': timedelta(0), 'last_station': None} for i in range(num_employees)]

    # Распределение начальных заявок
    assign_initial_tasks(task_objects, employees)

    # Распределение оставшихся заявок
    assign_remaining_tasks(task_objects, employees, G, labels)

    # Вывод информации о распределении заявок
    for task in task_objects:
        print(f"Заявка {task.id}: Сотрудник {task.employee_id}, {task.start_station} -> {task.end_station}, "
              f"Начало: {task.start_time}, Окончание: {task.end_time}")

    print('\n')
    for employee in employees:
        print(f"Сотрудник {employee['id']} выполнил {employee['task_count']} задач.")


# Запуск основной функции
if __name__ == "__main__":
    main()
