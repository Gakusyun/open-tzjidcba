import os
import json


def get_max_id():
    # 获取指定目录下的所有json文件，然后返回最大的id
    max_id = 0
    for filename in os.listdir("products"):
        if filename.endswith(".json"):
            filepath = os.path.join("products", filename)
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                id = data["id"]
                if id > max_id:
                    max_id = id
    return max_id + 1


def make_product(name, price, directory="./products"):
    # 生成一个商品并保存到指定目录
    id = get_max_id()
    data = {"id": id, "name": name, "price": price}
    file_path = os.path.join(directory, f"{id}_{name}.json")

    # 检查文件是否已存在
    if os.path.exists(file_path):
        print(f"商品文件 {file_path} 已存在，请使用不同的ID或名称。")
        return None

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return id


if __name__ == "__main__":
    name = input("请输入商品名称：")
    price = int(input("请输入商品售价："))
    id = make_product(name, price)
    if id is not None:
        print(f"生成成功，id为{id}，文件名为{id}_{name}.json")
