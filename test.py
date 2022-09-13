from threading import Thread
from time import sleep

def fun1():
    while True:
        print("1")
        sleep(2)

def fun2():
    while True:
        print("2")
        sleep(3)


t1 = Thread(target=fun1)
t2 = Thread(target=fun2)

t1.start()
t2.start()

t1.join()
t2.join()