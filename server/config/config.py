import os
import pathlib
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = pathlib.Path(__file__).parent.parent

CONFIG = {
    "APP_PORT": os.environ.get("APP_PORT"),
    "POSTGRES_HOST": os.environ.get("POSTGRES_HOST"),
    "POSTGRES_USER": os.environ.get("POSTGRES_USER"),
    "POSTGRES_DB": os.environ.get("POSTGRES_DB"),
    "POSTGRES_PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
    "POSTGRES_PORT": os.environ.get("POSTGRES_PORT"),
    "REDIS_HOST": os.environ.get("REDIS_HOST"),
    "REDIS_PORT": os.environ.get("REDIS_PORT"),
}
