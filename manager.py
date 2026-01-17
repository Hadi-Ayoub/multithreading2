from multiprocessing.managers import BaseManager
from queue import Queue

task_queue = Queue()
result_queue = Queue()


class QueueManager(BaseManager):
    pass


# Register queues for the server
QueueManager.register("get_task_queue", callable=lambda: task_queue)
QueueManager.register("get_result_queue", callable=lambda: result_queue)


class QueueClient:
    """Interface used by Boss and Minion"""

    def __init__(self):
        QueueManager.register("get_task_queue")
        QueueManager.register("get_result_queue")

        self.manager = QueueManager(address=("localhost", 50000), authkey=b"secret")
        self.manager.connect()

        self.task_queue = self.manager.get_task_queue()
        self.result_queue = self.manager.get_result_queue()


if __name__ == "__main__":
    print("Manager starting on port 50000...")
    manager = QueueManager(address=("", 50000), authkey=b"secret")
    server = manager.get_server()
    server.serve_forever()
