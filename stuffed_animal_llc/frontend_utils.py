import requests

def add_edge_request(source, target, message):
    edge_id = 'e'  + str(source) + '-' + str(target)
    body = {
        "id": edge_id,
        "source": str(source),
        "target": str(target),
        "animated": True,
        "type": "customEdge",
        "data": {"label": message}
    }
    url = "http://127.0.0.1:5000/addedge"
    resp = requests.post(url, json=body)

def action_request(source, action):
    body = {
        "source": str(source),
        "target": str(source),
        "data": {"label": action}
    }
    url = "http://127.0.0.1:5000/action"
    resp = requests.post(url, json=body)
        

def initial_request(message):
    body = {
        "ask": message,
    }
    url = "http://127.0.0.1:5000/setInitialAsk"
    resp = requests.post(url, json=body)

def end_request_thread():
    url = "http://127.0.0.1:5000/askFinished"
    resp = requests.post(url)