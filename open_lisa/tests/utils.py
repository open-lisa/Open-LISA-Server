import os
import shutil


def reset_databases():
    # Copy the seed files to the files that are used by the repositories
    shutil.copy("data_test/database/instruments.db.seed.json",
                "data_test/database/instruments.db.json")
    shutil.copy("data_test/database/commands.db.seed.json",
                "data_test/database/commands.db.json")
