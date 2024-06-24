from os import getenv
from dotenv import load_dotenv

load_dotenv()

user_database_uri = getenv("USER_DB_URI")
orchestrator_database_uri = getenv("ORC_DB_URI")

region_name = getenv("AWS_REGION")
aws_access_key_id = getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = getenv("AWS_SECRET_ACCESS_KEY")
aws_cluster = getenv("AWS_CLUSTER")
