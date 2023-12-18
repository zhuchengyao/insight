import json
import requests


def sales_data_update(action, volumn, city):
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({"action": action, "volumn": volumn, "city": city})
    r = requests.post("https://bugplatform.bixin.cn/bi/update", data=data, headers=headers)
    print(r.text)
