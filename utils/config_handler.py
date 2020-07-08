from configparser import ConfigParser
from config.public_data import config_path

class ConfigParse(object):
    def __init__(self):
        pass

    @classmethod
    def get_db_config(cls):
        cls.cf = ConfigParser()
        cls.cf.read(config_path)
        host = cls.cf.get("mysqlconf", "host")
        port = cls.cf.get("mysqlconf", "port")
        user = cls.cf.get("mysqlconf", "user")
        password = cls.cf.get("mysqlconf", "password")
        db = cls.cf.get("mysqlconf", "db_name")
        return {"host":host, "port":port, "user":user, "password":password,"db":db}