import traceback

import os
import sys

root_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.join(root_dir, "scripts"))


def get_path(filename):
    return os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), filename))

from easy_chat import EasyChatApp

try:
    EasyChatApp().run()
except Exception:
    error = traceback.format_exc()

    with open(get_path("ERROR.log"), "w") as error_file:
        error_file.write(error)

    print(error)