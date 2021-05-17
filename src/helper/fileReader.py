

import json
import os


class FileExtensions:

    @staticmethod
    def readFile(path, fileType='json'):
        #  Opening JSON file
        f = open(path, encoding='UTF-8')

        def readJsonFile(file):
            return json.load(file)

        options = {
            'json': readJsonFile(f)
        }

        return options[fileType]

    @staticmethod
    def fileExists(path) -> bool:
        return os.path.exists(path)
