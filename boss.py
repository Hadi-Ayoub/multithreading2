from manager import QueueClient
from task import Task
import time


def main():
    client = QueueClient()
    print("Boss connected")
    NUM_TASKS = 10
    SIZE = 1000

    # submit tasks
    print(f"Submitting {NUM_TASKS} tasks...")
    for i in range(NUM_TASKS):
        t = Task(i, SIZE)
        client.task_queue.put(t)

    # collect results
    print("Waiting for results...")
    start = time.perf_counter()

    for _ in range(NUM_TASKS):
        res = client.result_queue.get()
        print(f"Result: Task {res.identifier} (Time: {res.time:.4f}s)")

    print(f"Total processing time: {time.perf_counter() - start:.4f}s")


if __name__ == "__main__":
    main()
