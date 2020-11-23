from multiprocessing import Process, Queue
from time import sleep

from timeit import default_timer as timer


def run_cpu_tasks_in_parallel(func, objs):
    queue = Queue()
    queue.put({})
    running_tasks = [Process(target=func, args=(obj, queue,)) for obj in objs]
    for running_task in running_tasks:
        running_task.start()
    for running_task in running_tasks:
        running_task.join()
    return queue.get()


class MyClass:
    def __init__(self, name, start, end, time):
        self.steps = [e for e in range(start, end)]
        self.time = time
        self.name = name
        self.res = 'toto'

    def run(self, queue):
        t0 = timer()
        c = 1

        for e in self.steps:
            c += e
            t1 = timer()
            print(f'{self.name} step={e} c={c} t={t1-t0:.2f} s')
            sleep(self.time)

        self.res = c

        t1 = timer()
        print(f'{self.name} done in {t1-t0:.2f} s')

        q = queue.get()
        q[self.name] = self.res
        queue.put(q)


a = MyClass('A', 1, 6, 1)
b = MyClass('B', 0, 2, 2)
c = MyClass('C', 10, 12, 3)
objs = [a, b, c]


def worker(obj, queue):
    obj.run(queue)


res = run_cpu_tasks_in_parallel(worker, objs)

print(f'res: {res}')

for obj in objs:
    print(f'{obj.name}: {obj.res}')
