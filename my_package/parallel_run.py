from multiprocessing import Process, Queue


class ParallelRun:

    def __init__(self, func, objs):
        self.func = func
        self.objs = objs

    def run(self):
        queue = Queue()
        queue.put({})
        running_tasks = [Process(target=self.func, args=(obj, queue,)) for obj in self.objs]

        for running_task in running_tasks:
            running_task.start()

        for running_task in running_tasks:
            running_task.join()

        self.res = queue.get()

    def get_res(self):
        return self.res
