import json
import os
from pathlib import Path
import re


class CmdHelper:

    @staticmethod
    def waitWhileExpectedInput(expectedInput: re.Pattern[str],message: str="", fileType='json') -> str:
        exit = input(message)
        while (re.match(expectedInput,exit) == None):
            exit = input(message)
        
        return exit

    @staticmethod
    def fileExists(path: str) -> bool:
        onlyDirectoryPath = os.path.dirname(path)
        Path(onlyDirectoryPath).mkdir(parents=True, exist_ok=True)
        return os.path.exists(path)

    # Hint for the suffix of the color code: https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters
    # Hint for the color itself: https://en.wikipedia.org/wiki/ANSI_escape_code#Colors

    @staticmethod
    def print_colors_256(color_):
        print("\nThe 256 colors scheme is:")
        print(' '.join([CmdHelper.colors_256(x) for x in range(256)]))
        
    @staticmethod
    def colors_256(color_):
        num1 = str(color_)
        num2 = str(color_).ljust(3, ' ')
        if color_ % 16 == 0:
            return(f"\033[38;5;{num1}m {num2} \033[0;0m\n")
        else:
            return(f"\033[38;5;{num1}m {num2} \033[0;0m")

    class FGColor:
        BLACK = '\033[38;5;0m'
        RED = '\033[38;5;9m'
        GREEN = '\033[38;5;10m'
        YELLOW = '\033[38;5;11m'
        BLUE = '\033[38;5;12m'
        MAGENTA = '\033[38;5;13m'
        CYAN = '\033[38;5;14m'
        WHITE = '\033[38;5;15m'
        UNDERLINE = '\033[4m'
        RESET = '\033[0m'
    
    class BGColor:
        BLACK = '\033[48;5;0m'
        RED = '\033[48;5;9m'
        GREEN = '\033[48;5;10m'
        YELLOW = '\033[48;5;11m'
        BLUE = '\033[48;5;12m'
        MAGENTA = '\033[48;5;13m'
        CYAN = '\033[48;5;14m'
        WHITE = '\033[48;5;15m'
        UNDERLINE = '\033[4m'
        RESET = '\033[0m'

