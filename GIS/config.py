import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    DATABASE = os.path.join(BASE_DIR,"instance", "gear.db")