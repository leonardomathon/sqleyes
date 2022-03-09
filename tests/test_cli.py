import os
import pytest

def test_entrypoint():
    exit_status = os.system('sqleyes --help')
    assert exit_status == 0

