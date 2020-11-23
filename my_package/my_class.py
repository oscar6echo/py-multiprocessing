from time import sleep

from timeit import default_timer as timer


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
