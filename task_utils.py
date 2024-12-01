import json
import networkx as nx
import codecs
import matplotlib.pyplot as plt
from datetime import timedelta


def load_json_data(file_path):
    """Загружает JSON-данные из указанного файла."""
    with codecs.open(file_path, "r", "utf_8_sig") as file:
        return json.load(file)


def build_station_dict(stops):
    """Создает словарь соответствия узлов (nodeId) и станций (stationId)."""
    return {stop['nodeId']: stop['stationId'] for stop in stops}


def build_graph(nodes, links):
    """Создает граф на основе узлов и связей с учетом времени на каждой связи."""
    G = nx.Graph()
    for node in nodes:
        G.add_node(node['id'])
    for link in links:
        G.add_edge(link['fromNodeId'], link['toNodeId'], length=link['attributes']['time'])
    return G


def remove_unconnected_nodes(G):
    """Удаляет узлы с числом связей менее 2 для упрощения графа."""
    nodes_to_remove = [node for node in G.nodes() if len(G.edges(node)) < 2]
    G.remove_nodes_from(nodes_to_remove)
    return G


def build_labels_dict(names, node_station_dict):
    """Создает словарь названий станций по идентификаторам узлов."""
    labels = {}
    for node, station_id in node_station_dict.items():
        labels[node] = names['keysets']['generated'].get(station_id + '-name', {}).get('ru', 'error')
    return labels


def calc_time(G, st1, st2):
    """Рассчитывает время в пути между двумя станциями по их идентификаторам."""
    try:
        return round(nx.dijkstra_path_length(G, source=st1, target=st2, weight="length") / 60)
    except nx.NetworkXNoPath:
        return None


def find_station_id(labels, station_name):
    """Находит идентификатор узла по названию станции."""
    for node_id, name in labels.items():
        if name.lower() == station_name.lower():
            return node_id
    return None


class Task:
    """Класс для представления задачи."""
    task_counter = 1

    def __init__(self, ss, es, st, G, labels):
        self.id = Task.task_counter
        self.start_station = ss
        self.end_station = es
        self.start_time = timedelta(hours=st.hour, minutes=st.minute)
        self.end_time = self.calculate_end_time(G, labels)
        self.employee_id = None
        Task.task_counter += 1

    def calculate_end_time(self, G, labels):
        """Вычисляет время завершения задачи на основе графа и времени пути между станциями."""
        st1_id = find_station_id(labels, self.start_station)
        st2_id = find_station_id(labels, self.end_station)
        duration_minutes = calc_time(G, st1_id, st2_id)

        if duration_minutes is not None:
            return self.start_time + timedelta(minutes=duration_minutes)
        else:
            return self.start_time


def assign_initial_tasks(tasks, employees):
    """Назначает начальную задачу каждому сотруднику."""
    for i, task in enumerate(tasks[:len(employees)]):
        task.employee_id = employees[i]['id']
        employees[i]['available_time'] = task.end_time
        employees[i]['last_station'] = task.end_station
        employees[i].setdefault('task_count', 0)  # Инициализация счётчика задач
        employees[i]['task_count'] += 1


def find_best_employee_for_task(task, employees, G, labels):
    """Находит сотрудника, который быстрее всех сможет добраться до станции отправления задачи."""
    min_travel_time = timedelta.max
    best_employee = None

    for employee in employees:
        travel_time = timedelta(hours=0, minutes=calc_time(G, find_station_id(labels, employee['last_station']),
                                                  find_station_id(labels, task.start_station)))
        arrival_time = employee['available_time'] + travel_time

        if arrival_time < task.start_time and travel_time < min_travel_time:
            min_travel_time = travel_time
            best_employee = employee

    return best_employee


def assign_remaining_tasks(tasks, employees, G, labels):
    """Распределяет оставшиеся задачи, выбирая сотрудника с минимальным временем прибытия на место."""
    for task in tasks[len(employees):]:
        best_employee = find_best_employee_for_task(task, employees, G, labels)

        if best_employee:
            task.employee_id = best_employee['id']
            best_employee['available_time'] = task.end_time
            best_employee['last_station'] = task.end_station
            best_employee.setdefault('task_count', 0)  # Инициализация счётчика задач
            best_employee['task_count'] += 1