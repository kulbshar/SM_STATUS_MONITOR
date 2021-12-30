"""Tool to push msgs to the client (pull)"""
import zmq


class Publisher:

    def __init__(self):
        port = "5556"
        context = zmq.Context()
        self.socket = context.socket(zmq.PAIR)
        self.socket.connect("tcp://127.0.0.1:%s" % port)

    def send_json(self, msg):
        self.socket.send_json(msg)
