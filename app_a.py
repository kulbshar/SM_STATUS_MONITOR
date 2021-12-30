"""Application that produces a msg."""

from pairclient import Publisher

TABLE_NAME = "ldp_system_usage"


if __name__ == "__main__":

    my_msg = {
        "TABLE_NAME": "ldp_system_usage",
        "log_values": {"host": "mw", "status": "ERROR", "app": "a"}
    }
    pub = Publisher()
    pub.send_json(my_msg)
