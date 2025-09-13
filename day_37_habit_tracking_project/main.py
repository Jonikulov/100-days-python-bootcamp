"""Day 37. Habit Tracking Project"""

import requests

PIXELA_TOKEN = ""
PIXELA_USERNAME = ""

pixela_endpoint = "https://pixe.la/v1/users"
user_params = {
    "token": PIXELA_TOKEN,
    "username": PIXELA_USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}
# resp = requests.post(pixela_endpoint, json=user_params)
# print(resp)
# print(resp.text)


graph_endpoint = f"{pixela_endpoint}/{PIXELA_USERNAME}/graphs"
headers = {"X-USER-TOKEN": PIXELA_TOKEN}
payload = {
    "id": "graph1",
    "name": "Cycling",
    "unit": "km",
    "type": "float",
    "color": "momiji",
}
# resp = requests.post(graph_endpoint, headers=headers, json=payload)
# print(resp)
# print(resp.text)


entry_endpoint = f"{pixela_endpoint}/{PIXELA_USERNAME}/graphs/graph1"
payload = {
    "date": "20250903",
    "quantity": "3.7"
}
resp = requests.post(entry_endpoint, headers=headers, json=payload)
print(resp)
print(resp.text)


entry_endpoint = f"{pixela_endpoint}/{PIXELA_USERNAME}/graphs/graph1/20250903"
payload = {
    "quantity": "4.5"
}
# resp = requests.put(entry_endpoint, headers=headers, json=payload)
# print(resp)
# print(resp.text)


entry_endpoint = f"{pixela_endpoint}/{PIXELA_USERNAME}/graphs/graph1/20250831"
# resp = requests.delete(entry_endpoint, headers=headers)
# print(resp)
# print(resp.text)
