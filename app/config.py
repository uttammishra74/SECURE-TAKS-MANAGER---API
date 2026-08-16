import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("DB_HOST", "host.docker.internal")
user = os.getenv("DB_USER", "root")
name = os.getenv("DB_NAME", "secure_task_manager")
password = os.getenv("DB_PASSWORD", "")
port = os.getenv("DB_PORT", "3306")
