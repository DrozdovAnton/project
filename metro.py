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

plan = []
# plan: [idt, ide, ss, es, sth, stm, eth, etm]
# idt - identifier task
# ide - identifier employee
# ss - start station
# es - end station
# sth - start time hour
# stm - start time min
# eth - end time hour
# etm - end time min

def calc_between_t(ss, es, sth, stm):
    eth = etm = 0
    for i in paths:
        if ss + es == i[0] + i[1] or es + ss == i[0] + i[1]:
            eth = (sth + i[2]) % 24 + (stm + i[3]) // 60
            etm = (stm + i[3]) % 60
    return eth, etm

def determination_task(num_empl, plan):
    empl_and_path = []
    # empl_and_path: [ide, pth, ptm]
    # ide - identifier employee
    # pth - path time hour
    # ptm - path time min

    for i in range(len(plan)):
        # plan: [idt, ide, ss, es, sth, stm, eth, etm]
        if plan[i][0] == None:
            print(calc_between_t(plan[i-1][3],plan[i][2],plan[i-1][6],plan[i-1][7]))
            print(calc_between_t(plan[i-2][3],plan[i][2],plan[i-2][6],plan[i-2][7]))
    
tasks = sorted(tasks, key=itemgetter(2, 3))
num_employees = 2

for i in range(len(tasks)):
    # plan: [idt, ide, ss, es, sth, stm, eth, etm]
    plan.append(None)
    if len(tasks) >= num_employees and i < num_employees:
        plan[i] = i+1, i+1 ,tasks[i][0], tasks[i][1], tasks[i][2], tasks[i][3], calc_between_t(tasks[i][0], tasks[i][1], tasks[i][2], tasks[i][3])[0], calc_between_t(tasks[i][0], tasks[i][1], tasks[i][2], tasks[i][3])[1]
    else:
        plan[i] = i+1, None ,tasks[i][0], tasks[i][1], tasks[i][2], tasks[i][3], calc_between_t(tasks[i][0], tasks[i][1], tasks[i][2], tasks[i][3])[0], calc_between_t(tasks[i][0], tasks[i][1], tasks[i][2], tasks[i][3])[1]

for i in plan:
    print(i)