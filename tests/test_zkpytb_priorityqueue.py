#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the `utils` module of `zkpytb` package."""

import pytest

from zkpytb.priorityqueue import (
    EmptyQueueError,
    PriorityQueue,
)


def test_priority_queue_add_pop_task():
    pq = PriorityQueue()
    assert len(pq) == 0
    assert pq.empty
    tasks = [
        (999, 'last'),
        (10, 'to be replaced'),
        (5, 'middle'),
        (5, 'to be removed'),
        (1, 'first'),
        (5, 'middle2'),
        (-1, 'before first'),
    ]
    for prio, task in tasks:
        pq.add_task(task, prio)
    assert not pq.empty
    assert len(pq) == 7
    assert pq.entry_finder['to be replaced'][0] == 10
    pq.add_task('to be replaced', 88)
    assert len(pq) == 7
    assert pq.entry_finder['to be replaced'][0] == 88
    pq.remove_task('to be removed')
    assert len(pq) == 6
    assert pq.pop_task() == 'before first'
    assert pq.pop_task() == 'first'
    assert pq.pop_task() == 'middle'
    assert pq.pop_task() == 'middle2'
    assert pq.pop_task() == 'to be replaced'
    assert pq.pop_task() == 'last'
    assert len(pq) == 0
    with pytest.raises(EmptyQueueError) as excinfo:
        pq.pop_task()
    assert excinfo.value.args[0] == 'pop from an empty priority queue'
    assert pq.empty


def test_priority_queue_iter():
    pq = PriorityQueue(name='test_iter')
    assert pq.name == 'test_iter'
    tasks = [
        (999, 'last'),
        (5, 'middle'),
        (1, 'first'),
        (5, 'middle2'),
        (-1, 'before first'),
    ]
    for prio, task in tasks:
        pq.add_task(task, prio)
    expected_tasks = [
        'before first',
        'first',
        'middle',
        'middle2',
        'last',
    ]
    i = 0
    for task in pq:
        assert task == expected_tasks[i]
        i += 1
