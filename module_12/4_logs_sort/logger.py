import requests
import time
from datetime import datetime
from threading import Thread, Lock
from queue import Queue


class LogProcessor:
    def __init__(self):
        self.log_lock = Lock()
        self.queue = Queue()
        self.threads = []

    def get_current_timestamp(self, timestamp):
        """ Получение текущей даты и времени с сервера """
        response = requests.get(f"http://127.0.0.1:8080/timestamp/{timestamp}")
        if response.status_code == 200:
            return response.text
        else:
            return None

    def write_log(self, timestamp, date):
        """ Запись лога в файл """
        log_line = f"{timestamp} {date}"
        with self.log_lock:
            with open("logs.txt", "a") as file:
                file.write(log_line + "\n")

    def worker(self):
        """ Поток обработки таймштампов """
        while True:
            timestamp = self.queue.get()
            if timestamp is None:
                break
            current_timestamp = time.time()
            date = self.get_current_timestamp(current_timestamp)
            if date is None:
                break
            self.write_log(current_timestamp, date)
            time.sleep(1)
            self.queue.task_done()

    def process(self, start_timestamp, num_threads):
        """ Запуск обработки таймштампов """
        for i in range(num_threads):
            thread = Thread(target=self.worker)
            thread.start()
            self.threads.append(thread)

        for i in range(num_threads):
            self.queue.put(start_timestamp + i)

        self.queue.join()

        for _ in range(num_threads):
            self.queue.put(None)
        for thread in self.threads:
            thread.join()


if __name__ == "__main__":
    processor = LogProcessor()
    start_timestamp = int(time.time())
    num_threads = 10
    processor.process(start_timestamp, num_threads)
