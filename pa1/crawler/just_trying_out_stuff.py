import threading
import time
import urllib.robotparser
#https://docs.python.org/3/library/urllib.robotparser.html

x = 0

def thread_task(lock):
    global x
    for i in range(1000000):
        lock.acquire()
        x += 1
        lock.release()

def main_task1():

    lock = threading.Lock()

    t1 = threading.Thread(target=thread_task, args=(lock, ))
    t2 = threading.Thread(target=thread_task, args=(lock, ))

    t1.start()
    t2.start()

    t1.join()
    t2.join()



if __name__ == "__main__":
    main_task1()
    print(x)
    #print(time.time())
