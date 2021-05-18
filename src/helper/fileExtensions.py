

import json
import os
from pathlib import Path


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
    def fileExists(path: str) -> bool:
        onlyDirectoryPath = os.path.dirname(path)
        Path(onlyDirectoryPath).mkdir(parents=True, exist_ok=True)
        return os.path.exists(path)
