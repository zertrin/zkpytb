#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the `utils` module of `zkpytb` package."""

import os
import pytest
import subprocess
from pathlib import Path


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
    hash_res3 = hashstring(b'test', hash_method=a_hash_method)
    assert all(isinstance(res, str) for res in [hash_res1, hash_res2, hash_res3])
    assert all(len(res) > 0 for res in [hash_res1, hash_res2, hash_res3])
    assert hash_res1 != hash_res2
    assert hash_res2 == hash_res3


def test_hashfile_hashmethods(a_hash_method, tmp_path: Path):
    f1 = tmp_path / "hashfile1.txt"
    f2 = tmp_path / "hashfile2.txt"
    f3 = tmp_path / "hashfile3.txt"
    f1.write_text("content1")
    f2.write_text("content2")
    f3.write_text("content2")
    hashfile_res1 = hashfile(f1, hash_method=a_hash_method)
    hashfile_res2 = hashfile(f2, hash_method=a_hash_method)
    hashfile_res3 = hashfile(f3, hash_method=a_hash_method)
    assert all(isinstance(res, str) for res in [hashfile_res1, hashfile_res2, hashfile_res3])
    assert all(len(res) > 0 for res in [hashfile_res1, hashfile_res2, hashfile_res3])
    assert hashfile_res1 != hashfile_res2
    assert hashfile_res2 == hashfile_res3


@pytest.mark.xfail(reason="Tox temp dir is located under the main git repository of the project...")
def test_get_git_hash_nogit(tmp_path: Path):
    curdir = Path.cwd()
    try:
        nogit_dir = (tmp_path / "nogit_dir").mkdir()
        assert nogit_dir is not None
        os.chdir(nogit_dir)
        git_hash = get_git_hash()
    finally:
        os.chdir(curdir)

    assert git_hash == ''


def test_get_git_hash_emptygit(tmp_path: Path):
    curdir = Path.cwd()
    try:
        emptygit_dir: Path = tmp_path / "emptygit_dir"
        emptygit_dir.mkdir()
        os.chdir(emptygit_dir)
        subprocess.check_call(['git', 'init'])
        git_hash = get_git_hash()
    finally:
        os.chdir(curdir)

    assert git_hash == ''


def test_get_git_hash_minimalgit(tmp_path: Path):
    curdir = Path.cwd()
    try:
        minimalgit_dir: Path = tmp_path / "minimalgit_dir"
        minimalgit_dir.mkdir()
        (minimalgit_dir / 'testfile.txt').write_text('minimalgit')
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
