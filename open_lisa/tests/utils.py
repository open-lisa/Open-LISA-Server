import shutil
import json
import sys
import os


def reset_databases():
    # delete current directories state
    if os.path.exists("data_test/database"):
        shutil.rmtree("data_test/database")
    if os.path.exists("data_test/clibs"):
        shutil.rmtree("data_test/clibs", ignore_errors=True)
    if os.path.exists("data_test/sandbox"):
        shutil.rmtree("data_test/sandbox")


    # Copy the seed folders to the folders that Open LISA manages
    shutil.copytree(os.path.join(os.getcwd(), "data_test/database_seed"),
                    os.path.join(os.getcwd(), "data_test/database"))

    shutil.copytree(os.path.join(os.getcwd(), "data_test/clibs_seed"),
                    os.path.join(os.getcwd(), "data_test/clibs"), dirs_exist_ok=True)

    shutil.copytree(os.path.join(os.getcwd(), "data_test/sandbox_seed"),
                        os.path.join(os.getcwd(), "data_test/sandbox"))

    if sys.platform.startswith('win'):
        try:
            with open(os.path.join(os.getcwd(), "data_test/database/commands.db.json")) as file:
                db = json.load(file)
                for command in db["data"]:
                    if command["metadata"]:
                        if "lib_file_name" in command["metadata"]:
                            command["metadata"]["lib_file_name"] = command["metadata"]["lib_file_name"].replace(".dll",
                                                                                                                "_x86.dll")

            with open(os.path.join(os.getcwd(), "data_test/database/commands.db.json"), "wt") as file:
                file.write(json.dumps(db, indent=4))

        except Exception as e:
            print(e)
