import requests
r = requests.post("http://127.0.0.1:5000/paste", json={"content":"hello","expiry":1})
print(r.json())

g = requests.get(f"http://127.0.0.1:5000/paste/{r.json()['id']}")
print(g.json())
