import time
from threading import Thread
g = [1,1]
def work1(g):
    while True:
        time.sleep(1)
        print(g)

def work2(g):
    time.sleep(5)
    g.append(3)
    
t1 = Thread(target=work1, args=(g,))
t1.start()

t2 = Thread(target=work2, args=(g,))
t2.start()


