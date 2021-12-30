import zmq
import time
from lp_log import LPLogger

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://127.0.0.1:%s" % port)


while True:
    msg = socket.recv_json()
    print(msg)

    logger = LPLogger(msg)
    logger.log_msg()
    logger.close()
    time.sleep(1)
