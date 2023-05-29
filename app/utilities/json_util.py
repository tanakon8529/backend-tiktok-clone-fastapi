import json

class json_controls(object):
    def __init__(self):
        self.blabla = ''

    def read_json_file(self, path):
        try:
            file = open(path)
            data = json.load(file)
            return data
        except Exception as e:
            return e
        finally:
            file.close
    
    def write_json_file(self, path, data):
        json_obj = json.dumps(data)

        with open(path, "w") as outfile:
            outfile.write(json_obj)