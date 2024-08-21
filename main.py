import os
import json
import random


class Gamer(object):
    def __init__(self, huihe=0, cash=100000, inventory={}):
        self.inventory = inventory
        self.cash = cash
        self.huihe = huihe

    def print_inventory(self):
        print("玩家库存：{}".format(self.inventory))
        print("玩家现金：{}".format(self.cash))


class Product(object):
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price


def load_products():
    products = []
    for filename in os.listdir("products"):
        if filename.endswith(".json"):
            filepath = os.path.join("products", filename)
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                product = Product(data["id"], data["name"], data["price"])
                products.append(product)
    return products


def news(products):
    if random.randint(0, 9) % 2 == 0:
        print("今年市场平稳")
    else:
        for product in products:
            flag = random.randint(1, 9)
            if flag % 3 == 0:
                print("{}大跌".format(product.name))
                product.price /= random.randint(2, 3)
            elif flag % 3 == 2:
                print("{}大涨".format(product.name))
                product.price *= random.randint(9, 11)


def start_game():
    if os.path.exists("player.json"):
        with open("player.json", "r") as file:
            data = json.load(file)
            player = Gamer(**data)
            if input("已有存档，是否继续游戏(y/n):") == "n":
                player = Gamer()
    else:
        player = Gamer()
    i = player.huihe
    while i <= 70:
        products = load_products()
        print("第{}回合".format(i + 1))
        for product in products:
            product.price *= random.uniform(0.75, 1.25)
        news(products)
        for product in products:
            product.price = int(product.price)
            print("{}: {} 价格：{}".format(product.id, product.name, product.price))
        player.print_inventory()
        while True:
            print("请选择卖出还是购买")
            print("1.购买")
            print("2.卖出")
            print("-1.下一个回合")
            choice = input("请输入你的选择:")
            if choice == "1":
                while True:
                    choice = input("请输入你要购买的商品id(-1退出):")
                    if choice in [str(product.id) for product in products]:
                        print(
                            "你最多可以买{}份{}".format(
                                int(player.cash / products[int(choice)].price),
                                products[int(choice)].name,
                            )
                        )
                        much = int(
                            input(
                                "请输入你要购买{}的数量:".format(
                                    products[int(choice)].name
                                )
                            )
                        )
                        if much == 0:
                            continue
                        if products[int(choice)].name in player.inventory:
                            if player.cash >= much * products[int(choice)].price:
                                player.cash -= much * products[int(choice)].price
                                player.inventory[products[int(choice)].name] += much
                                print("购买成功")
                                player.print_inventory()
                            else:
                                print("余额不足")
                        else:
                            if player.cash >= much * products[int(choice)].price:
                                player.cash -= much * products[int(choice)].price
                                player.inventory[products[int(choice)].name] = much
                                print("购买成功")
                                player.print_inventory()
                            else:
                                print("余额不足")
                        continue
                    elif choice == "-1":
                        print()
                        break
                    else:
                        print("输入错误，请重新输入")
                        continue
            elif choice == "2":
                while True:
                    choice = input("请输入你要卖出的商品id(-1退出):")
                    if choice in [str(product.id) for product in products]:
                        print(
                            "你最多可以卖{}份{}".format(
                                player.inventory[products[int(choice)].name],
                                products[int(choice)].name,
                            )
                        )
                        much = int(
                            input(
                                "请输入你要卖出的{}的数量:".format(
                                    products[int(choice)].name
                                )
                            )
                        )
                        if much == 0:
                            continue
                        if much <= player.inventory[products[int(choice)].name]:
                            player.cash += much * products[int(choice)].price
                            player.inventory[products[int(choice)].name] -= much
                            if player.inventory[products[int(choice)].name] == 0:
                                del player.inventory[products[int(choice)].name]
                            print("卖出成功")
                            player.print_inventory()
                        else:
                            print("库存不足")
                            continue
                    elif choice == "-1":
                        print()
                        break
                    else:
                        print("输入错误，请重新输入")
                        continue
            elif choice == "-1":
                print()
                break
            else:
                print("输入错误，请重新输入")
        i += 1
        player.huihe = i
        with open("player.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(player.__dict__))


def upgrade():
    print("升级功能暂未开发")
    main()


def main():
    print("欢迎来到《投机倒把》")
    print("这是一个简易的模拟经营类游戏")
    print("1.开始游戏")
    print("2.升级")
    print("3.退出游戏")
    print("4.关于")
    choise = int(input("请选择："))
    if choise == 1:
        start_game()
        exit()
    elif choise == 2:
        upgrade()
        exit()
    elif choise == 3:
        exit()
    elif choise == 4:
        print("作者：Gakusyun")
        print("邮箱：gaoxj040620@gmail.com")
        print("https://github.com/Gakusyun/open-tzjidcba")
        input("按 Enter 键继续...")
        main()


if __name__ == "__main__":
    main()
