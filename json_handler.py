import json

def save_json(file_path, data, mode='w'):
    with open(file_path, mode) as file:
        json.dump(data, file, indent=4)

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
      
    except FileNotFoundError:
        return None
    
def clean_json(file_path):
    with open(file_path, 'w') as file:
        json.dump({}, file, indent=4)

def dump_json(file_path):
    return json.dumps(file_path, indent=4)