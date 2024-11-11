from datetime import time, timedelta
from operator import itemgetter


paths=[["Медведково","Бабушкинская",0,4],["Медведково","Свиблово",0,6],["Медведково","Ботанический сад",0,8],["Медведково","ВДНХ",0,12],["Медведково","Алексеевская",0,15],["Медведково","Рижская",0,17],["Медведково","Проспект мира",0,20],["Бабушкинская","Свиблово",0,3],["Бабушкинская","Ботанический сад",0,6],["Бабушкинская","ВДНХ",0,10],["Бабушкинская","Алексеевская",0,12],["Бабушкинская","Рижская",0,14],["Бабушкинская","Проспект мира",0,17],["Свиблово","Ботанический сад",0,3],["Свиблово","ВДНХ",0,7],["Свиблово","Алексеевская",0,10],["Свиблово","Рижская",0,12],["Свиблово","Проспект мира",0,15],["Ботанический сад","ВДНХ",0,5],["Ботанический сад","Алексеевская",0,7],["Ботанический сад","Рижская",0,10],["Ботанический сад","Проспект мира",0,12],["ВДНХ","Алексеевская",0,3],["ВДНХ","Рижская",0,6],["ВДНХ","Проспект мира",0,8],["Алексеевская","Рижская",0,3],["Алексеевская","Проспект мира",0,6],["Рижская","Проспект мира",0,4]]
# path: [ss, es, pth, ptm]
# ss - start station
# es - end station
# pth - path time hour
# ptm - path time min

tasks = []
# task: [ss, es, sth, stm]
# ss - start station
# es - end station
# sth - start time hour
# stm - start time min

plan = [] # list of Task
num_employees = 2

class Task:
    idt = 1
    def __init__(self, ss, es, st):
        # idt - id task
        # ide - id employee
        # ss - start station
        # es - end station
        # st - start time
        # et - end time

        self.idt = Task.idt 
        self.ide = None
        self.ss = ss
        self.es = es
        self.st = st
        self.et = self.set_et()

        Task.idt += 1

    def set_et(self):
        for i in paths:
            if self.ss + self.es == i[0] + i[1] or self.es + self.ss == i[0] + i[1]:
                return timedelta(hours=i[2], minutes=i[3]) + timedelta(hours=self.st.hour, minutes=self.st.minute)
                
    def get_all_info(self):
        print(self.idt, self.ide, self.ss, self.es, self.st, self.et, '\n')

def get_time_path(ss, es):
    for p in paths:
        if ss + es == p[0] + p[1] or es + ss == p[0] + p[1]:
            return time(p[2], p[3])
        elif ss == es:
            return time(0, 0)

def set_ide():
    for task in plan:
        task.ide = None
    
    for i in range(len(plan)):
        if i < num_employees:
            plan[i].ide = i+1

    for i in range(len(plan)):
        if plan[i].ide == None:
            path_time_and_id_e = []
        
            for j in range(num_employees):
                path_time_and_id_e.append([timedelta(hours=get_time_path(plan[i-(j+1)].es, plan[i].ss).hour, minutes=get_time_path(plan[i-(j+1)].es, plan[i].ss).minute) + plan[i-(j+1)].et, plan[i-(j+1)].ide])
            path_time_and_id_e = sorted(path_time_and_id_e, key=itemgetter(0))
            
            if path_time_and_id_e[0][0] < timedelta(hours=plan[i].st.hour, minutes=plan[1].st.minute):
                plan[i].ide = path_time_and_id_e[0][1]

def add_task(ss, es, h, m):
    plan.append(Task(ss, es, time(h, m)))
    plan.sort(key=lambda plan: plan.st)
    set_ide()