import json
import codecs
from traceback import print_tb

import networkx as nx
from collections import Counter

# Открытие JSON файлов с использованием `with open` для автоматического закрытия
with codecs.open("l10n.json", "r", "utf_8_sig") as f:
    names = json.load(f)

with codecs.open("data.json", "r", "utf_8_sig") as f:
    graph = json.load(f)

# Создание словаря соответствия `nodeId` и `stationId`
nodeStdict = {stop['nodeId']: stop['stationId'] for stop in graph['stops']['items']}

# Инициализация графа и добавление узлов и рёбер
G = nx.Graph()
G.add_nodes_from(node['id'] for node in graph['nodes']['items'])  # Добавление узлов
G.add_edges_from(
    (link['fromNodeId'], link['toNodeId'], {'length': link['attributes']['time']})
    for link in graph['links']['items']
)  # Добавление рёбер с атрибутом "длина"

# Создание словаря станций {id: 'название станции'}
stations = {}
for node in G.nodes():
    station_id = nodeStdict.get(node)
    if station_id:  # Проверка, что station_id существует
        station_name = names['keysets']['generated'].get(f"{station_id}-name", {}).get('ru')
        if station_name:
            stations[node] = station_name

# Подсчитываем количество каждого значения
value_counts = Counter(stations.values())

# Создаем новый словарь с уникальными значениями
unique_stations = {k: v for k, v in stations.items() if value_counts[v] == 1}

# Оставляем только уникальные названия станций
station_names = list(set(unique_stations.values()))

# Записываем уникальные названия в новый файл
with open('unique_stations.txt', 'w', encoding='utf-8') as f:
    for name in station_names:
        f.write(name + ' ')

# Находим идентификатор станции по частичному имени
def find_station_by_name(partial_name, station_names):
    partial_name = partial_name.lower()
    matches = [station_name for station_name in station_names if partial_name in station_name.lower()]

    if len(matches) == 1:
        return matches[0]  # Возвращаем единственное найденное название
    elif len(matches) > 1:
        print("Найдено больше 1 станции, уточните запрос")
        return None  # Возвращаем None, так как найдено несколько станций
    else:
        return None  # Возвращаем None, если станции не найдены

# Вычисляем время с использованием предвычисленных данных
def calc_time(station_name_1, station_name_2, res):
    # Находим идентификаторы станций по именам
    st1 = find_station_by_name(station_name_1, station_names)
    st2 = find_station_by_name(station_name_2, station_names)

    # Проверяем, что обе станции найдены
    if st1 is None or st2 is None:
        return None

    # Проверяем наличие пути в предвычисленных данных и возвращаем время
    if st1 in res and st2 in res[st1]:
        time_in_minutes = res[st1][st2] / 60  # делим на 60 для перевода в минуты
        return round(time_in_minutes)
    else:
        return None

with codecs.open("stations_time.json", "r", "utf_8_sig") as f:
    res = json.load(f)


if __name__ == '__main__':
    src_station = 'вднх'
    dst_station = 'коломенская'
    time = calc_time(src_station, dst_station, res)
    print(unique_stations)
    print(station_names)
    print(len(unique_stations))
    print(len(station_names))

    if time is not None:
        print(f'Время от {src_station} до {dst_station}: {time} минут(ы)')
    else:
        print(f'Не удалось найти путь между {src_station} и {dst_station}')
