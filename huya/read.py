import json
with open('datas.json',encoding="utf-8") as file_obj:
    datas = json.load(file_obj)
print(datas)
print(len(datas))