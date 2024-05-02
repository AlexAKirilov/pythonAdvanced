from threading import Semaphore, Thread
import time
import signal

sem: Semaphore = Semaphore()
stop_threads = False


def signal_handler(sig, frame):
    global stop_threads
    print("\nReceived keyboard interrupt, quitting threads.")
    stop_threads = True


def fun1():
    global stop_threads
    while not stop_threads:
        sem.acquire()
        print(1)
        sem.release()
        time.sleep(0.25)


def fun2():
    global stop_threads
    while not stop_threads:
        sem.acquire()
        print(2)
        sem.release()
        time.sleep(0.25)


t1: Thread = Thread(target=fun1)
t2: Thread = Thread(target=fun2)

signal.signal(signal.SIGINT, signal_handler)

try:
    t1.start()
    t2.start()
    t1.join()
    t2.join()
except KeyboardInterrupt:
    pass
