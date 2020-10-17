from food import Food
name = ["保鲜室1", "保鲜室2", "保鲜室3", "保鲜室4", "保鲜室5", "保鲜室6"]
temp = [0, 0, 0, 0, 0, 0]
mois = [80, 80, 80, 80, 80, 80]
Type = ["默认", "默认", "默认", "默认", "默认", "默认"]
info = ["箱体清空，已恢复默认模式！", "箱体清空，已恢复默认模式！", "箱体清空，已恢复默认模式！", "箱体清空，已恢复默认模式！", "箱体清空，已恢复默认模式！", "箱体清空，已恢复默认模式！"]
note = ["无通知。", "无通知。", "无通知。", "无通知。", "无通知。", "无通知。"]
colo = ["white", "white", "white", "white", "white", "white"]
fruit_list = ['fruit', 'apple', 'banana', 'orange', 'peach', 'pear', 'berry', 'pineapple', 'melon', 'radish', 'tomato', 'cucumber', 'pumpkin']
vegetable_list = ['vegetable', 'carrot', 'broccoli', 'mushroom', 'spinach', 'celery', 'caraway', 'lettuce', 'agaric', 'lotus root', 'water shield', 'arrowhead', 'cress']
meat_list = ['meat', 'beef', 'pork', 'fish', 'egg', 'mutton', 'chicken', 'duck']
drinking_list = ['drinking', 'milk', 'yogurt', 'coke', 'beer', 'vodka', 'donut', 'pizza', 'hot dog']
food_database = [fruit_list, vegetable_list, meat_list, drinking_list]
temperature_reco = [10, 3, 0, 5]
moisture_reco = [95, 95, 85, 90]
Typename = ["水果与喜温蔬菜", "喜凉蔬菜", "禽畜肉与蛋", "甜点，饮品"]

def find_food(foodname):
    if foodname in fruit_list:
        return Food(foodname, fruit_list[0], 0)
    elif foodname in vegetable_list:
        return Food(foodname, vegetable_list[0], 1)
    elif foodname in meat_list:
        return Food(foodname, meat_list[0], 2)
    elif foodname in drinking_list:
        return Food(foodname, drinking_list[0], 3)
    else:
        # print("请选择食材类型:\n")
        # print("1. 水果、根茎菜、瓜果菜、豆\n")
        # print("2. 叶菜、菌菇、水生蔬菜\n")
        # print("3. 禽肉、畜肉、蛋、鱼\n")
        # print("4. 饮料、奶制品、酒类、甜点\n")
        # str = input()
        # food_database[int(str)-1].append(foodname)
        return 0
def classify(food_list):
    group = [["水果或喜温蔬菜","",0],["喜凉蔬菜","",0],["禽畜肉与蛋","",0],["甜点或饮品","",0],[]]
    food_list = list(set(food_list))
    for food in food_list:
        Food = find_food(food)
        if Food != 0:
            group[Food.num][1] = group[Food.num][1] + " " + Food.name
            group[Food.name][2] += 1
    for i in range(4):
        if group[i][2] != 0:
            group[4].append(i)
    return group
class Tank:

    def __init__(self):
        self.attribute = 'empty'
        self.containing_food_list = []

    def check(self, food_list):
        group = classify(food_list)
        info = food_list
        self.containing_food_list = food_list
        if self.check_empty():
            if len(group[4]) == 0:
                note = "无通知。"
                info = "箱体清空，已恢复默认模式！"
            if len(group[4]) == 1:
                note = "保鲜仓环境设置成功！"
                self.containing_food_list = food_list
                info = group[group[4][0]][0] + ": " + group[group[4][0]][1]
                self.attribute = group[group[4][0]][0]
        else:
            if len(group[4]) == 0:
                note = "无通知。"
                info = "箱体清空，已恢复默认模式！"
                self.attribute = 'empty'
                self.containing_food_list = list()
            if len(group[4]) == 1:
                note = "食材状态更新成功！"
                self.containing_food_list = food_list
                info = group[group[4][0]][0] + ": " + group[group[4][0]][1]
                self.attribute = group[group[4][0]][0]
        if len(group[4]) == 2:
                note = "不建议将{}{}和{}{}放入同一保鲜仓内，它们所需的最佳保鲜环境不同。".format(group[group[4][0]][0],group[group[4][0]][1],group[group[4][1]][0],group[group[4][1]][1])
        if len(group[4]) == 3:
                note = "不建议将{}{},{}{}以及{}{}放入同一保鲜仓内，它们所需的最佳保鲜环境不同。".format(group[group[4][0]][0],group[group[4][0]][1],group[group[4][1]][0],group[group[4][0]][1],group[group[4][2]][0],group[group[4][2]][1])
        if len(group[4]) == 4:
                note = "不建议将{}{},{}{},{}{}以及{}{}放入同一保鲜仓内，它们所需的最佳保鲜环境不同。".format(group[group[4][0]][0],group[group[4][0]][1],group[group[4][1]][0],group[group[4][0]][1],group[group[4][2]][0],group[group[4][2]][1],group[group[4][3]][0],group[group[4][3]][1])
        return info, note


    def add_food(self, new_foodlist):
        info = ""
        color = "yellow"
        if len(new_foodlist) > 0:
            for foodname, foodquantity in new_foodlist:
                new_food = find_food(foodname)
                if new_food != 0:
                    if self.check_empty():
                        # self.containing_food_list.append(new_food)
                        self.attribute = new_food.attribute
                        info += "创建新仓：{}\n".format(new_food.attribute)
                    if new_food.attribute == self.attribute:
                        self.containing_food_list.append(new_food)
                        info += "{:d}个{}添加成功！\n".format(foodquantity, new_food.name)
                    else:
                        self.containing_food_list.append(new_food)
                        info += "{}不应该放置在此箱体，建议取走！\n".format(new_food.name)
                        color = "red"
        return [info, color]

    def remove_food(self, food_list):
        info = ""
        if len(food_list) > 0:
            for foodname, foodquantity in food_list:
                for i in range(foodquantity):
                    for food in self.containing_food_list:
                        if foodname == food.name:
                            self.containing_food_list.remove(food)
                            info += "{}已取出！\n".format(food.name)
            if len(self.containing_food_list) == 0:
                self.attribute = 'empty'
                print("保鲜仓清空，已恢复默认模式！")
        return info

    def remove_all(self):
        self.attribute = 'empty'
        self.containing_food_list = []
        print("箱体清空，已恢复默认模式！")

    def check_empty(self):
        if len(self.containing_food_list) == 0:
            return True
        else:
            return False

    def print_content(self):
        print("----------")
        for food in self.containing_food_list:
            print(food.name)
        print("舱体类型：{}".format(self.attribute))
        