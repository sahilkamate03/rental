import os
from dotenv import load_dotenv

load_dotenv(".env")

RUN_MODE = os.getenv("RUN_MODE")
FERNET_KEY = os.getenv("FERNET_KEY")

# DATABASE
DB_TYPE = os.getenv("DB_TYPE")

if DB_TYPE == "PROD":
    DB_SERVER = os.getenv("DB_SERVER")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PWD = os.getenv("DB_PWD")

else:
    DB_SERVER = os.getenv("DB_SERVER_LOCAL")
    DB_NAME = os.getenv("DB_NAME_LOCAL")
    DB_USER = os.getenv("DB_USER_LOCAL")
    DB_PWD = os.getenv("DB_PWD_LOCAL")

SQL_ACLCHEMY_KEY = os.getenv("SQL_ACLCHEMY_KEY")


