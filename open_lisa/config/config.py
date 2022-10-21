from dotenv import load_dotenv
import os
import logging
from pathlib import Path


def load_config(env):
    cfg_path = os.path.join(os.path.dirname(__file__), "{}.env".format(env))
    logging.info(
        "[OpenLISA][load_config] - Loading env variables from {}".format(cfg_path))
    load_dotenv(cfg_path)

    # create folders if they no exist
    logging.info(
        "[OpenLISA][load_config] - creating folders")
    Path(os.getenv("DATABASE_FOLDER")).mkdir(parents=True, exist_ok=True)
    Path(os.getenv("CLIBS_FOLDER")).mkdir(parents=True, exist_ok=True)
    Path(os.getenv("USER_FILES_FOLDER")).mkdir(parents=True, exist_ok=True)
