from datetime import time, timedelta
from operator import itemgetter


paths=[["Медведково","Бабушкинская",0,4],["Медведково","Свиблово",0,6],["Медведково","Ботанический сад",0,8],["Медведково","ВДНХ",0,12],["Медведково","Алексеевская",0,15],["Медведково","Рижская",0,17],["Медведково","Проспект мира",0,20],["Бабушкинская","Свиблово",0,3],["Бабушкинская","Ботанический сад",0,6],["Бабушкинская","ВДНХ",0,10],["Бабушкинская","Алексеевская",0,12],["Бабушкинская","Рижская",0,14],["Бабушкинская","Проспект мира",0,17],["Свиблово","Ботанический сад",0,3],["Свиблово","ВДНХ",0,7],["Свиблово","Алексеевская",0,10],["Свиблово","Рижская",0,12],["Свиблово","Проспект мира",0,15],["Ботанический сад","ВДНХ",0,5],["Ботанический сад","Алексеевская",0,7],["Ботанический сад","Рижская",0,10],["Ботанический сад","Проспект мира",0,12],["ВДНХ","Алексеевская",0,3],["ВДНХ","Рижская",0,6],["ВДНХ","Проспект мира",0,8],["Алексеевская","Рижская",0,3],["Алексеевская","Проспект мира",0,6],["Рижская","Проспект мира",0,4]]
# path: [ss, es, pth, ptm]
# ss - start station
# es - end station
# pth - path time hour
# ptm - path time min

tasks = [["Ботанический сад","Рижская",13,40],["Алексеевская","Рижская",10,30],["Проспект мира","Свиблово",10,50],["Ботанический сад","ВДНХ",17,30],["Свиблово","Проспект мира",12,00],["Алексеевская","Медведково",14,50],["Алексеевская","Бабушкинская",12,15],["Алексеевская","ВДНХ",16,50],["ВДНХ","Проспект мира",17,20],["Свиблово","Алексеевская",18,00]]
# task: [ss, es, sth, stm]
# ss - start station
# es - end station
# sth - start time hour
# stm - start time min
tasks = sorted(tasks, key=itemgetter(2, 3))

plan = [] # list of Task

num_employees = 2

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
                
    def get_all_info(self):
        print(self.idt, self.ide, self.ss, self.es, self.st, self.et)

# def set_ide():


for i in tasks:
    plan.append(Task(i[0], i[1], time(i[2], i[3])))

# idt - ide

for i in plan:
    i.get_all_info()