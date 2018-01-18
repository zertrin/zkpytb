"""
Miscellaneous helper functions

Author: Marc Gallet
Date: 2017-06
"""

import hashlib
import heapq
import itertools
import logging
import subprocess


mylogger = logging.getLogger('zkpytb.utils')


def hashfile(filepath, hash_method='sha256', BLOCKSIZE=65536):
    """Hash a file"""

    hasher = hashlib.new(hash_method)

    with open(str(filepath), 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)

    return hasher.hexdigest()


def hashstring(inputstring, hash_method='sha256'):
    """Hash a file"""

    hasher = hashlib.new(hash_method)
    hasher.update(inputstring)
    return hasher.hexdigest()


def get_git_hash(rev='HEAD'):
    """Get the git hash of the current directory"""

    git_hash = ''
    try:
        git_out = subprocess.check_output(['git', 'rev-parse', rev], universal_newlines=True)
    except subprocess.CalledProcessError as e:
        mylogger.exception("Couldn't determine the git hash!")
    else:
        git_hash = git_out.strip()

    return git_hash


class PriorityQueue:
    """From https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes"""
    def __init__(self):
        self.pq = []                         # list of entries arranged in a heap
        self.entry_finder = {}               # mapping of tasks to entries
        self.REMOVED = '<removed-task>'      # placeholder for a removed task
        self.counter = itertools.count()     # unique sequence count

    def add_task(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.pq, entry)

    def remove_task(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task = heapq.heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')
