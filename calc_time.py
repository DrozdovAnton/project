import json
import codecs
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

def find_station_id_by_name(partial_name, unique_stations):
    partial_name = partial_name.lower()
    matches = [node_id for node_id, station_name in unique_stations.items() if partial_name in station_name.lower()]

    if len(matches) == 1:
        return matches[0]  # Возвращаем единственный найденный идентификатор
    elif len(matches) > 1:
        print(f"Найдено больше 1 станций, уточните запрос")
        return None  # Возвращаем None, так как найдено несколько станций
    else:
        return None  # Возвращаем None, если станции не найдены

def calc_time(station_name_1, station_name_2):
    # Находим идентификаторы станций по именам
    st1 = find_station_id_by_name(station_name_1, unique_stations)
    st2 = find_station_id_by_name(station_name_2, unique_stations)

    # Проверяем, что обе станции найдены
    if st1 is None:
        return None
    if st2 is None:
        return None

    # Вычисляем время с использованием Dijkstra
    time_in_minutes = nx.dijkstra_path_length(G, source=st1, target=st2, weight="length") / 60
    return round(time_in_minutes)


if __name__ == '__main__':

    src_station = 'вднх'
    dst_station = 'красносельская'
    time = calc_time(src_station, dst_station)

    print(f'Время от {src_station} до {dst_station} {time} минут(ы)')