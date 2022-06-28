from dotenv import load_dotenv
import os


print("set to none")
OPEN_LISA_CFG = None


def load_config(env):
    cfg_path = "{}/{}.env".format(os.path.dirname(__file__), env)
    load_dotenv(cfg_path)
