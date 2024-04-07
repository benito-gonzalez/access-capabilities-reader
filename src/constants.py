import os

my_path = os.path.abspath(os.path.dirname(__file__))
APP_PATH = os.path.join(my_path, "..")
DATA_PATH = os.path.join(APP_PATH, "data")
DB_PATH = os.path.join(APP_PATH, "chroma_db")
