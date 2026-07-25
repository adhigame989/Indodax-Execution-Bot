import os

APP_NAME = "Indodax Execution Bot"
VERSION = "1.0.0"

HOST = "0.0.0.0"
PORT = int(os.getenv("PORT", 5000))

DATA_DIR = "data"

UPDATE_INTERVAL = 2

DEBUG = False

API_KEY = os.getenv("API_KEY", "")

API_SECRET = os.getenv("API_SECRET", "")
