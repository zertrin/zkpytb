#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `zkpytb` package."""

import os
import pytest
import subprocess


from zkpytb.utils import (
    hashfile,
    hashstring,
    get_git_hash,
)


@pytest.fixture(scope='module',
                params='sha512,sha256,sha1,md5'.split(','))
def a_hash_method(request):
    return request.param


def test_hashstring_hashmethods(a_hash_method):
    hash_res1 = hashstring(b'', hash_method=a_hash_method)
    hash_res2 = hashstring(b'test', hash_method=a_hash_method)
    assert isinstance(hash_res1, str)
    assert len(hash_res1) > 0
    assert hash_res1 != hash_res2


def test_hashfile_hashmethods(a_hash_method, tmpdir):
    f1 = tmpdir.join("hashfile1.txt")
    f2 = tmpdir.join("hashfile2.txt")
    f1.write("content1")
    f2.write("content2")
    hashfile_res1 = hashfile(f1, hash_method=a_hash_method)
    hashfile_res2 = hashfile(f2, hash_method=a_hash_method)
    assert isinstance(hashfile_res1, str)
    assert len(hashfile_res1) > 0
    assert hashfile_res1 != hashfile_res2


@pytest.mark.xfail(reason="Tox temp dir is located under the main git repository of the project...")
def test_get_git_hash_nogit(tmpdir):
    curdir = os.getcwd()
    try:
        nogit_dir = tmpdir.mkdir("nogit_dir")
        os.chdir(str(nogit_dir))
        git_hash = get_git_hash()
    finally:
        os.chdir(curdir)

    assert git_hash == ''


def test_get_git_hash_emptygit(tmpdir):
    curdir = os.getcwd()
    try:
        emptygit_dir = tmpdir.mkdir("emptygit_dir")
        os.chdir(str(emptygit_dir))
        subprocess.check_call(['git', 'init'])
        git_hash = get_git_hash()
    finally:
        os.chdir(curdir)

    assert git_hash == ''


def test_get_git_hash_minimalgit(tmpdir):
    curdir = os.getcwd()
    try:
        minimalgit_dir = tmpdir.mkdir("minimalgit_dir")
        minimalgit_dir.join('testfile.txt').write('minimalgit')
        os.chdir(str(minimalgit_dir))
        subprocess.check_call(['git', 'init'])
        subprocess.check_call(['git', 'config', 'user.email', 'test@domain.invalid'])
        subprocess.check_call(['git', 'config', 'user.name', 'Test User'])
        subprocess.check_call(['git', 'add', 'testfile.txt'])
        subprocess.check_call(['git', 'commit', '-m', 'testcommit'])
        git_hash = get_git_hash()
    finally:
        os.chdir(curdir)

    assert isinstance(git_hash, str)
    assert len(git_hash) == 40
