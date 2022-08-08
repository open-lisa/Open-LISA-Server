from distutils.dir_util import copy_tree, remove_tree
import json
import sys
import os


def reset_databases():
    # delete current directories state
    remove_tree("data_test/database")
    remove_tree("data_test/clibs")
    remove_tree("data_test/sandbox")

    # Copy the seed folders to the folders that Open LISA manages
    copy_tree(os.path.join(os.getcwd(), "data_test/database_seed"),
              os.path.join(os.getcwd(), "data_test/database"))

    copy_tree(os.path.join(os.getcwd(), "data_test/clibs_seed"),
              os.path.join(os.getcwd(), "data_test/clibs"))

    copy_tree(os.path.join(os.getcwd(), "data_test/sandbox_seed"),
              os.path.join(os.getcwd(), "data_test/sandbox"))

    if sys.platform.startswith('win'):
        try:
            with open(os.path.join(os.getcwd(), "data_test/database/commands.db.json")) as file:
                db = json.load(file)
                for command in db["data"]:
                    if "lib_file_name" in command:
                        command["lib_file_name"] = command["lib_file_name"].replace(
                            ".dll", "_x86.dll")

            with open(os.path.join(os.getcwd(), "data_test/database/commands.db.json"), "wt") as file:
                file.write(json.dumps(db, indent=4))

        except Exception as e:
            print(e)
