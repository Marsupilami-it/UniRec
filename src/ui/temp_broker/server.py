import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

queues = {}

while True:
    #  Wait for next request from client
    queue_name, data = socket.recv_pyobj()
    print("Received request:", queue_name, data)
    if data:
        queues.setdefault(queue_name, []).append(data)
    else:
        queue = queues.get(queue_name, [])
        if queue:
            data = queue.pop(0)
            socket.send_pyobj(data)

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    # socket.send(b"World")
