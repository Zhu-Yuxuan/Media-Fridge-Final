import threading
import detection
from tkinter import *
from tank import *
from food import Food
import time
import tkinter.font as tkFont

class GUI():
    def __init__(self, root):
        self.initGUI(root)
    def Update(self):
        global temp, mois, Type
        for i in range(2):
            self.content[2][i].config(text=Type[i], bg=colo[i])
            self.content[3][i].config(text=temp[i], bg=colo[i])
            self.content[4][i].config(text=mois[i], bg=colo[i])
            self.content[6][i].config(text=info[i], bg=colo[i])
            self.content[7][i].config(text=note[i], bg=colo[i])
            self.content[1][i][0].config(bg=colo[i])
            self.content[1][i][1].config(bg=colo[i])
            self.content[1][i][2].config(bg=colo[i])
            self.content[5][i][0].config(bg=colo[i])
            self.content[5][i][1].config(bg=colo[i])
            self.content[0][i].config(bg=colo[i])
            self.framelist[i].config(bg=colo[i])
        self.root.after(1000, self.Update)
    def initGUI(self, root):
        global temp, mois, Type
        self.root = root
        self.root.geometry("1024x600")
        self.root.title("Frodge UI")
        self.framelist = []
        self.content = [[], [], [], [], [], [], [], []]
        # init list
        for i in range(6):
            self.framelist.append(Frame())
            self.content[0].append(Label()) # name
            self.content[1].append([Label(), Label(), Label()])  # fix
            self.content[2].append(Label())  # Type
            self.content[3].append(Label())  # tempture
            self.content[4].append(Label())  # moisture
            self.content[5].append([Label(), Label()])  # unit
            self.content[6].append(Label()) # information
            self.content[7].append(Label()) # note
        # init frame
        for i in range(6):
            self.framelist[i] = Frame(self.root, height=300, width=341, bg=colo[i])
            self.framelist[i].grid_propagate(0)
            self.content[0][i] = Label(self.framelist[i], text=name[i], bg=colo[i], font="Fixdsys 15 bold") # name
            self.content[1][i][0] = Label(self.framelist[i], text="类型：", bg=colo[i], font="Fixdsys 12") # fixed properties
            self.content[1][i][1] = Label(self.framelist[i], text="温度：", bg=colo[i], font="Fixdsys 12")
            self.content[1][i][2] = Label(self.framelist[i], text="湿度：", bg=colo[i], font="Fixdsys 12")
            self.content[2][i] = Label(self.framelist[i], text=Type[i], bg=colo[i],font="Fixdsys 12") # Type
            self.content[3][i] = Label(self.framelist[i], text=temp[i], bg=colo[i],font="Fixdsys 12") # temperature
            self.content[4][i] = Label(self.framelist[i], text=mois[i], bg=colo[i],font="Fixdsys 12") # moisture
            self.content[5][i][0] = Label(self.framelist[i], text="°C", bg=colo[i],font="Fixdsys 12") # unit
            self.content[5][i][1] = Label(self.framelist[i], text="%", bg=colo[i],font="Fixdsys 12")
            self.content[6][i] = Label(self.framelist[i], text=info[i], bg=colo[i],font="Fixdsys 12") # information: food
            self.content[7][i] = Label(self.framelist[i], test=note[i], bg=colo[i],font="Fixdsys 12") # notification: warning, reminding
            self.content[0][i].grid(row=0, column=1, columnspan=3)
            self.content[1][i][0].grid(row=1, column=1)
            self.content[1][i][1].grid(row=2, column=1)
            self.content[1][i][2].grid(row=3, column=1)
            self.content[2][i].grid(row=1, column=2)
            self.content[3][i].grid(row=2, column=2)
            self.content[4][i].grid(row=3, column=2)
            self.content[5][i][0].grid(row=2 ,column=3)
            self.content[5][i][1].grid(row=3, column=3)
            self.content[6][i].grid(row=4, column=1, columnspan=3, pady = 15)
            self.content[7][i].grid(row=5,column=1, columnspan=3, pady = 15)
            self.framelist[i].grid(row=i // 3, column=i % 3)
        self.root.after(1000, self.Update)
        self.root.mainloop()

def fridgeUI():
    root = Tk()
    fUI = GUI(root)

def diff_n(listA, listB):
    listadd = list()
    for ele in listA:
        numA = listA.count(ele)
        numB = listB.count(ele)
        diffa = numA - numB
        if diffa > 0:
            listadd.append([ele, diffa])
    listadd = list(set(listadd))
    return listadd

def logic(fridge):
    while True:
        info[0], note[0] = fridge[0].check(detection.detection0)
        info[1], note[1] = fridge[1].check(detection.detection1)


# def logic1(fridge):
#     foodlist1_curr = list()
#     foodlist1_prev = list()
#     foodlist1_curr = detection.detection0
#     while True:
#         foodlist1_prev = foodlist1_curr
#         foodlist1_curr = detection.detection1
#         info[1], colo[1] = fridge.add_food(diff_n(foodlist1_curr, foodlist1_prev))
#         info[1] += fridge.remove_food(diff_n(foodlist1_prev, foodlist1_curr))
#         print(info[1])
#         if info[1] != "":
#             time.sleep(2.5)
        time.sleep(0.5)


def terminal_simu(fridge):
    while True:
        str = input ("命令：")
        if str[0] in ['1', '2', '3', '4', '5', '6']:
            if str[1] == '+':
                food = find_food(str[2:])
                if food.attribute == fridge[int(str[0])-1].attribute or fridge[int(str[0])-1].attribute == 'empty':
                    temp[int(str[0])-1] = temperature_reco[food.num]
                    mois[int(str[0])-1] = moisture_reco[food.num]
                    Type[int(str[0])-1] = Typename[food.num]
                    fridge[int(str[0])-1].add_food(food)
                else:
                    print("该食材不应该放置在此箱体！")
            elif str[1] == '-':
                fridge[int(str[0])-1].remove_food(find_food(str[2:]))
                if len(fridge[int(str[0])-1].containing_food_list) == 0:
                    temp[int(str[0])-1] = 0
                    mois[int(str[0])-1] = 80
                    Type[int(str[0])-1] = "默认"
            elif str[1:] == "check":
                for n in fridge[int(str[0])-1].containing_food_list:
                    print(n.name, " ")
            else:
                print("无效命令，请重新输入！")
        elif str == "quit":
            break
        else:
            print("无效命令，请重新输入！")

if __name__ == "__main__":
    fridge = [Tank(), Tank(), Tank(), Tank(), Tank(), Tank()]
    t1 = threading.Thread(target=fridgeUI)
    t2 = threading.Thread(target=logic, args=(fridge,))
    # t3 = threading.Thread(target=logic1, args=(fridge[1],))
    t4 = threading.Thread(target=detection.detect)
    t1.start()
    t2.start()
    # t3.start()
    t4.start()
