from config import user_database_uri, orchestrator_database_uri
import psycopg2


class UserSingleton:
    _instance = None

    def __new__(cls, user_database_url=user_database_uri):
        if cls._instance is None:
            cls._instance = super(UserSingleton, cls).__new__(cls)
            cls._instance.connection = psycopg2.connect(user_database_url)
            cls._instance.cursor = cls._instance.connection.cursor()

        return cls._instance


class OrcSingleton:
    _instance = None

    def __new__(cls, user_database_url=orchestrator_database_uri):
        if cls._instance is None:
            cls._instance = super(OrcSingleton, cls).__new__(cls)
            cls._instance.connection = psycopg2.connect(user_database_url)
            cls._instance.cursor = cls._instance.connection.cursor()

        return cls._instance
