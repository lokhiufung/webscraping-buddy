import json


class JsonlPipeline:
    def __init__(self, file_path):
        self.file_path = file_path

    def write(self, item):
        # append only writing
        with open(self.file_path, 'a') as f:
            f.write(json.dumps(item) + '\n')

    def batch_write(self, items):
        # append only writing
        with open(self.file_path, 'a') as f:
            f.writelines([json.dumps(item) + '\n' for item in items])
    