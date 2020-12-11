import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)
DEBUG = os.getenv("DEBUG", False)

if DEBUG:
    print("We are in debug")
    env_path = Path(".") / ".env.debug"
    load_dotenv(dotenv_path=env_path)
    from settings_files.Devolpment import *
else:
    print("We are in production")
    from settings_files.Production import *
