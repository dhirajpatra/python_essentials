import threading


def new():
    """
    This is a call back test method to call threading
    """
    for x in range(6):
        print("child executing..", threading.current_thread().name)


# thread using standard method
t1 = threading.Thread(target=new)
t1.start()
t1.join()
print("done", threading.current_thread().name)


# inheritance from threading class
class A(threading.Thread):
    def run(self):
        for x in range(6):
            print("child executing..", threading.current_thread().name)


objA = A()
objA.start()
objA.join()
print("control returned to main ", threading.current_thread().name)


# using instance method from a custom class
class ex():
    def B(self):
        lst = [5, 2, 7, 'good', 9, 'bad']
        for x in lst:
            print("child printing ", x)


objEx = ex()
t1 = threading.Thread(target=objEx.B)
t1.start()
t1.join()
print("done")
