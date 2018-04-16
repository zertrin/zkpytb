"""
An implementation of a priority queue based on heapq and
https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes

Author: Marc Gallet
Date: 2018-01
"""

import heapq
import itertools


class EmptyQueueError(Exception):
    pass


class PriorityQueue:
    """Based on https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes"""
    def __init__(self, name=''):
        self.name = name
        self.pq = []                         # list of entries arranged in a heap
        self.entry_finder = {}               # mapping of tasks to entries
        self.counter = itertools.count()     # unique sequence count
        self.num_tasks = 0                  # track the number of tasks in the queue

    def __len__(self):
        return self.num_tasks

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.pop_task()
        except EmptyQueueError:
            raise StopIteration

    @property
    def empty(self):
        return self.num_tasks == 0

    def add_task(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        removed = False
        entry = [priority, count, task, removed]
        self.entry_finder[task] = entry
        heapq.heappush(self.pq, entry)
        self.num_tasks += 1

    def remove_task(self, task):
        'Mark an existing task as REMOVED. Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = True  # mark the element as removed
        self.num_tasks -= 1

    def pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task, removed = heapq.heappop(self.pq)
            if not removed:
                del self.entry_finder[task]
                self.num_tasks -= 1
                return task
        raise EmptyQueueError('pop from an empty priority queue')
