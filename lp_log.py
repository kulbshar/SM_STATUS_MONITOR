"""Classes for creating log and adding to DB. """
import sqlite3
from typing import Dict






# imagine a more sophisticated object, where the table schema are defined and
# mapped to a name, then we can build thess as needed
class LPSystemUsage:

    DEFAULT_PATH = "/scharp/devel/mwillia3/test_log.log"

    def __init__(self, table_name="", path=None):
        self.table_name = table_name
        if path is None:
            self.path = self.DEFAULT_PATH
        else:
            self.path = path

    def build_dml(self, host="", status="", app=""):
        dml = (
            f"INSERT INTO {self.table_name} VALUES ('{host}', '{status}',"
            f" '{app}')"
        )
        return dml

    def build_ddl(self):
        ddl = f"CREATE TABLE {self.table_name} (host, status, app)"
        return ddl


# map all loggers here
lp_logs = {"ldp_system_usage": LPSystemUsage}


class LPLogger:

    def __init__(self, msg: Dict):

        table_name = msg["TABLE_NAME"]
        self.msg_content = msg["log_values"]

        LogBuilder = lp_logs[table_name]
        logger = LogBuilder(table_name)

        self.con = sqlite3.connect(logger.path)
        self.ddl = logger.build_ddl()
        self._build_table(self.ddl)

        self.dml = logger.build_dml(**self.msg_content)

    def _build_table(self, ddl: str):
        """Try building the DB unless it already exists"""
        try:
            self.con.execute(ddl)
        except sqlite3.OperationalError:
            pass

    def log_msg(self):
        """insert log into database."""
        self.con.execute(self.dml)
        self.con.commit()

    def close(self):
        self.con.close()
