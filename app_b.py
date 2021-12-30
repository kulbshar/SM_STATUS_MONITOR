"""Application that produces a msg."""

from pairclient import Publisher

TABLE_NAME = "ldp_system_usage"


def app_A():
    # runs the application
    my_msg = {
        "TABLE_NAME": TABLE_NAME,
        "log_values": {"host": "mw", "status": "ERROR", "app": "b"}
    }
    return my_msg


if __name__ == "__main__":

    my_msg = app_A()

    pub = Publisher()
    pub.send_json(my_msg)
