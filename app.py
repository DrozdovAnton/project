from flask import Flask, render_template, request, redirect, url_for
from datetime import timedelta, time
from operator import itemgetter
from task_utils import (load_json_data, build_station_dict, build_graph,
                        remove_unconnected_nodes, build_labels_dict,
                        find_station_id, Task, assign_initial_tasks, assign_remaining_tasks)

# Инициализация Flask приложения
app = Flask(__name__)

# Глобальные данные
tasks = []  # Список объектов Task
employees = []
num_employees = 3

stations = [
    "Авиамоторная", "Автозаводская", "Академическая", "Александровский сад",
    "Алексеевская", "Алма-Атинская", "Алтуфьево", "Аннино", "Арбатская", "Аэропорт",
    "Бабушкинская", "Багратионовская", "Баррикадная", "Бауманская", "Беговая",
    "Белорусская", "Беляево", "Бибирево", "Библиотека имени Ленина", "Битцевский парк",
    "Борисово", "Боровицкая", "Ботанический сад", "Братиславская",
    "Бульвар адмирала Ушакова", "Бульвар Дмитрия Донского", "Бульвар Рокоссовского",
    "Бунинская аллея", "Варшавская", "ВДНХ", "Владыкино", "Водный стадион", "Войковская",
    "Волгоградский проспект", "Волжская", "Волоколамская", "Воробьевы горы", "Выставочная",
    "Выхино", "Деловой центр", "Динамо", "Дмитровская", "Добрынинская", "Домодедовская",
    "Достоевская", "Дубровка", "Жулебино", "Зябликово", "Измайловская", "Калужская",
    "Кантемировская", "Каховская", "Каширская", "Киевская", "Китай-город", "Кожуховская",
    "Коломенская", "Комсомольская", "Коньково", "Красногвардейская", "Краснопресненская",
    "Красносельская", "Красные ворота", "Крестьянская застава", "Кропоткинская",
    "Крылатское", "Кузнецкий мост", "Кузьминки", "Кунцевская", "Курская", "Кутузовская",
    "Ленинский проспект", "Лермонтовский проспект", "Лесопарковая", "Лубянка", "Люблино",
    "Марксистская", "Марьина роща", "Марьино", "Маяковская", "Медведково", "Международная",
    "Менделеевская", "Митино", "Молодежная", "Выставочный центр", "Телецентр",
    "Улица Академика Королева", "Улица Милашенкова", "Улица Сергея Эйзенштейна",
    "Тимирязевская", "Мякинино", "Нагатинская", "Нагорная", "Нахимовский проспект",
    "Новогиреево", "Новокосино", "Новокузнецкая", "Новослободская", "Новоясеневская",
    "Новые Черемушки", "Октябрьская", "Октябрьское поле", "Орехово", "Отрадное",
    "Охотный ряд", "Павелецкая", "Парк культуры", "Парк Победы", "Партизанская",
    "Первомайская", "Перово", "Петровско-Разумовская", "Печатники", "Пионерская",
    "Планерная", "Площадь Ильича", "Площадь Революции", "Полежаевская", "Полянка",
    "Пражская", "Преображенская площадь", "Пролетарская", "Проспект Вернадского",
    "Проспект Мира", "Профсоюзная", "Пушкинская", "Пятницкое шоссе", "Речной вокзал",
    "Рижская", "Римская", "Рязанский проспект", "Савеловская", "Свиблово", "Севастопольская",
    "Семеновская", "Серпуховская", "Славянский бульвар", "Смоленская", "Сокол", "Сокольники",
    "Спартак", "Спортивная", "Сретенский бульвар", "Строгино", "Студенческая", "Сухаревская",
    "Сходненская", "Таганская", "Тверская", "Театральная", "Текстильщики", "Теплый стан",
    "Третьяковская", "Тропарево", "Трубная", "Тульская", "Тургеневская", "Тушинская",
    "Улица Академика Янгеля", "Улица Горчакова", "Улица Скобелевская",
    "Улица Старокачаловская", "Улица 1905 года", "Университет", "Филевский парк", "Фили",
    "Фрунзенская", "Царицыно", "Цветной бульвар", "Черкизовская", "Чертановская", "Чеховская",
    "Чистые пруды", "Чкаловская", "Шаболовская", "Шипиловская", "Шоссе Энтузиастов",
    "Щелковская", "Щукинская", "Электрозаводская", "Юго-Западная", "Южная", "Ясенево"
]

# Загрузка данных при запуске
names = load_json_data("l10n.json")
graph_data = load_json_data("data.json")
node_station_dict = build_station_dict(graph_data['stops']['items'])
G = build_graph(graph_data['nodes']['items'], graph_data['links']['items'])
G = remove_unconnected_nodes(G)
labels = build_labels_dict(names, node_station_dict)

def initialize_employees():
    global employees
    employees = [{'id': i + 1, 'available_time': timedelta(0), 'last_station': None, 'task_count': 0} for i in range(num_employees)]

@app.route('/load_data_test', methods=['GET', 'POST'])
def load_data_test():
    global tasks
    tasks_list = [["Ботанический сад", "Рижская", 9, 30], ["ВДНХ", "Проспект мира", 10, 45], ["Охотный ряд", "Театральная", 11, 15], ["Новокосино", "Шоссе Энтузиастов", 12, 0], ["Киевская", "Арбатская", 13, 20], ["Беговая", "Улица 1905 года", 14, 50], ["Речной вокзал", "Войковская", 15, 10], ["Южная", "Чертановская", 16, 30], ["Таганская", "Китай-город", 17, 5], ["Перово", "Новогиреево", 17, 45], ["Щёлковская", "Первомайская", 18, 15], ["Третьяковская", "Парк Культуры", 19, 0], ["Бабушкинская", "Свиблово", 20, 25], ["Лубянка", "Чистые пруды", 21, 40], ["Каширская", "Коломенская", 22, 30], ["Бабушкинская", "Таганская", 8, 45], ["Тропарёво", "Славянский бульвар", 9, 20], ["Юго-Западная", "Киевская", 10, 0], ["Площадь Ильича", "Каширская", 11, 30], ["Щукинская", "Парк Победы", 12, 15], ["Полежаевская", "Октябрьская", 13, 45]]
    tasks_list = sorted(tasks_list, key=itemgetter(2, 3))

    for t in tasks_list:
        st1_id = find_station_id(labels, t[0])
        st2_id = find_station_id(labels, t[1])

        if st1_id is not None and st2_id is not None:
            task = Task(t[0], t[1], time(t[2], t[3]), G, labels)
            tasks.append(task)

    tasks.sort(key=lambda x: x.start_time)

    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_task', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        start_station = request.form['start_station']
        end_station = request.form['end_station']
        start_hour = int(request.form['start_hour'])
        start_minute = int(request.form['start_minute'])

        st1_id = find_station_id(labels, start_station)
        st2_id = find_station_id(labels, end_station)

        if st1_id is not None and st2_id is not None:
            task_start_time = time(start_hour, start_minute)
            new_task = Task(start_station, end_station, task_start_time, G, labels)
            tasks.append(new_task)
            tasks.sort(key=lambda x: x.start_time)

        assign_remaining_tasks(tasks, employees, G, labels)
        return redirect(url_for('view_schedule'))

    return render_template('create_task.html', stations=stations)

@app.route('/assign_tasks', methods=['GET'])
def assign_tasks():
    # Распределение задач среди сотрудников
    initialize_employees()
    assign_initial_tasks(tasks, employees)
    assign_remaining_tasks(tasks, employees, G, labels)
    return redirect(url_for('index'))

@app.route('/view_schedule', methods=['GET'])
def view_schedule():
    return render_template('view_schedule.html', tasks=tasks, employees=employees)

@app.route('/clear_schedule', methods=['GET', 'POST'])
def clear_schedule():
    global tasks, employees
    tasks.clear()
    initialize_employees()  # Сброс данных о сотрудниках
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)