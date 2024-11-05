from datetime import time, timedelta
from operator import itemgetter

paths = [
    ["Медведково", "Бабушкинская", 0, 4], ["Медведково", "Свиблово", 0, 6], ["Медведково", "Ботанический сад", 0, 8], ["Медведково", "ВДНХ", 0, 12], ["Медведково", "Алексеевская", 0, 15], ["Медведково", "Рижская", 0, 17], ["Медведково", "Проспект мира", 0, 20],
    ["Бабушкинская", "Свиблово", 0, 3], ["Бабушкинская", "Ботанический сад", 0, 6], ["Бабушкинская", "ВДНХ", 0, 10], ["Бабушкинская", "Алексеевская", 0, 12], ["Бабушкинская", "Рижская", 0, 14], ["Бабушкинская", "Проспект мира", 0, 17],
    ["Свиблово", "Ботанический сад", 0, 3], ["Свиблово", "ВДНХ", 0, 7], ["Свиблово", "Алексеевская", 0, 10], ["Свиблово", "Рижская", 0, 12], ["Свиблово", "Проспект мира", 0, 15],
    ["Ботанический сад", "ВДНХ", 0, 5], ["Ботанический сад", "Алексеевская", 0, 7], ["Ботанический сад", "Рижская", 0, 10], ["Ботанический сад", "Проспект мира", 0, 12],
    ["ВДНХ", "Алексеевская", 0, 3], ["ВДНХ", "Рижская", 0, 6], ["ВДНХ", "Проспект мира", 0, 8],
    ["Алексеевская", "Рижская", 0, 3], ["Алексеевская", "Проспект мира", 0, 6],
    ["Рижская", "Проспект мира", 0, 4]
]

tasks = [
    ["Ботанический сад", "Рижская", 13, 40], ["Алексеевская", "Рижская", 10, 30], ["Проспект мира", "Свиблово", 10, 50], ["Ботанический сад", "ВДНХ", 17, 30], ["Свиблово", "Проспект мира", 12, 00], ["Алексеевская", "Медведково", 14, 50], ["Алексеевская", "Бабушкинская", 12, 15], ["Алексеевская", "ВДНХ", 16, 50], ["ВДНХ", "Проспект мира", 17, 20], ["Свиблово", "Алексеевская", 18, 00]
]

tasks = sorted(tasks, key=itemgetter(2, 3))

plan = []  # list of Task

num_employees = 4

class Task:
    idt = 1

    def __init__(self, ss, es, st):
        self.idt = Task.idt
        self.ide = self.set_ide_default()
        self.ss = ss
        self.es = es
        self.st = st
        self.et = self.set_et()

        Task.idt += 1

    def set_et(self):
        for i in paths:
            if self.ss + self.es == i[0] + i[1] or self.es + self.ss == i[0] + i[1]:
                return timedelta(hours=i[2], minutes=i[3]) + timedelta(hours=self.st.hour, minutes=self.st.minute)

    def set_ide_default(self):
        if self.idt <= num_employees:
            return self.idt
        return None

    def get_all_info(self):
        print(self.idt, self.ide, self.ss, self.es, self.st, self.et)

def calc_time(t1, t2):
    return timedelta(t1 + t2)

def get_time_path(ss, es):
    for p in paths:
        if ss + es == p[0] + p[1] or es + ss == p[0] + p[1]:
            return time(p[2], p[3])
        elif ss == es:
            return time(0, 0)

def set_ide():
    for i in range(len(plan)):
        if plan[i].ide is None:
            available_employees = {j: timedelta(hours=0, minutes=0) for j in range(1, num_employees + 1)}
            for j in range(i):
                if plan[j].ide in available_employees:
                    travel_time = timedelta(hours=get_time_path(plan[j].es, plan[i].ss).hour, minutes=get_time_path(plan[j].es, plan[i].ss).minute)
                    available_employees[plan[j].ide] = max(available_employees[plan[j].ide], plan[j].et + travel_time)

            earliest_available = min(available_employees.items(), key=lambda x: x[1])
            if earliest_available[1] <= timedelta(hours=plan[i].st.hour, minutes=plan[i].st.minute):
                plan[i].ide = earliest_available[0]

for i in tasks:
    plan.append(Task(i[0], i[1], time(i[2], i[3])))

for i in plan:
    set_ide()
    i.get_all_info()