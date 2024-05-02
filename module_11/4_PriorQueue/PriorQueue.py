import threading
import time
from queue import PriorityQueue

class Task:
    def __init__(self, priority):
        self.priority = priority

    def __str__(self):
        return f"Task(priority={self.priority})."

class Producer(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        print("Producer: Running")
        tasks = [
            Task(0),
            Task(2),
            Task(1),
            Task(4),
            Task(3),
            Task(6),
        ]

        for task in tasks:
            self.queue.put((task.priority, task))
            time.sleep(0.5)

        print("Producer: Done")

class Consumer(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        print("Consumer: Running")
        while True:
            priority, task = self.queue.get()
            if task is None:
                self.queue.task_done()
                break
            print(f"> {task}          sleep({priority * 0.1})")
            time.sleep(priority * 0.1)
            self.queue.task_done()

        print("Consumer: Done")

def main():
    queue = PriorityQueue()
    producer = Producer(queue)
    consumer = Consumer(queue)

    producer.start()
    consumer.start()

    producer.join()
    queue.put((None, None))
    queue.join()
    consumer.join()

if __name__ == "__main__":
    main()