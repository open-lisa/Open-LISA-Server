import json
import sys
import os
import shutil


def reset_databases():
    # Copy the seed files to the files that are used by the repositories
    shutil.copy(os.path.join(os.getcwd(), "data_test/database/instruments.db.seed.json"), os.path.join(os.getcwd(), "data_test/database/instruments.db.json"))
    shutil.copy(os.path.join(os.getcwd(), "data_test/database/commands.db.seed.json"), os.path.join(os.getcwd(), "data_test/database/commands.db.json"))

    if sys.platform.startswith('win'):
        try:
            with open(os.path.join(os.getcwd(), "data_test/database/commands.db.json")) as file:
                commands = json.load(file)
                for command in commands:
                    if "lib_file_name" in command:
                        command["lib_file_name"] = command["lib_file_name"].replace(".dll", "_86.dll")
        except Exception as e:
            print(e)



