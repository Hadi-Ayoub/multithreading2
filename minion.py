from manager import QueueClient


def main():
    client = QueueClient()
    print("Minion connected")

    while True:
        try:
            task = client.task_queue.get()
            print(f"Processing task {task.identifier} (size {task.size})...")

            task.work()

            client.result_queue.put(task)
            print(f"Task {task.identifier} done in {task.time:.4f}s")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
