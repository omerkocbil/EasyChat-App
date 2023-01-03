import traceback

from easy_chat import EasyChatApp

try:
    EasyChatApp().run()
except Exception:
    error = traceback.format_exc()

    with open("ERROR.log", "w") as error_file:
        error_file.write(error)

    print(error)