import json

def read_config() -> dict:
    with open('config.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def save_config(tree):
    with open('config.json', 'w', encoding='utf-8') as file:
        conf = {}
        for item_id in tree.get_children():
            item = tree.item(item_id)
            conf[item['values'][5]] = {
                "group_name": item['values'][0],
                "member_start_id": item['values'][1],
                "member_end_id":item['values'][2],
                "msg": item['values'][3],
                "sleep": item['values'][4],
                "profile": item['values'][5],
            }
        file.write(json.dumps(conf))