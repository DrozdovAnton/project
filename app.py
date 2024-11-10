from flask import Flask, render_template, request, redirect, url_for
from task_scheduler import Task, assign_initial_tasks, assign_remaining_tasks, load_json_data, build_station_dict, build_graph, remove_unconnected_nodes, build_labels_dict
from datetime import time, timedelta

app = Flask(__name__)

# Загружаем данные для графа
names = load_json_data("l10n.json")
graph_data = load_json_data("data.json")

node_station_dict = build_station_dict(graph_data['stops']['items'])
G = build_graph(graph_data['nodes']['items'], graph_data['links']['items'])
G = remove_unconnected_nodes(G)
labels = build_labels_dict(names, node_station_dict)

# Список всех задач
tasks_list = []


# Главная страница для создания заявки пользователями
@app.route('/')
def home():
    return render_template('user_form.html')


# Страница для работников
@app.route('/schedule')
def schedule():
    return render_template('worker_schedule.html', tasks=tasks_list)


# Обработка создания заявки
@app.route('/submit', methods=['POST'])
def submit_task():
    start_station = request.form['start_station']
    end_station = request.form['end_station']
    start_time = request.form['start_time']

    # Преобразование времени
    hour, minute = map(int, start_time.split(':'))
    task_obj = Task(start_station, end_station, time(hour, minute), G, labels)

    # Добавляем задачу в список
    tasks_list.append(task_obj)

    # Назначение задачи сотрудникам
    num_employees = 3
    employees = [{'id': i + 1, 'available_time': timedelta(0), 'last_station': None} for i in range(num_employees)]
    assign_initial_tasks(tasks_list, employees)
    assign_remaining_tasks(tasks_list, employees, G, labels)

    return redirect(url_for('schedule'))  # Перенаправление на страницу расписания


if __name__ == '__main__':
    app.run(debug=True)
