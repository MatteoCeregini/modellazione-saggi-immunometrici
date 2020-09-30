import json
import os


class JSONWriter:
    def __init__(self, data, path, file_name):
        self.data = data
        self.path = path
        self.file_name = file_name

    def write_json(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        with open(os.path.join(self.path, self.file_name), 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
