import json

def load_default():
    with open('default.json') as json_file:
        return json.load(json_file)
