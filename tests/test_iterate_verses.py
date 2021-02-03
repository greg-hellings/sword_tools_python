import pytest
from sword_tools_python import utils


@pytest.fixture
def kjv():
    return utils.get_mod("KJV")


def test_genesis_1_1(kjv):
    idx = 0
    expected = "In the beginning God created the heaven and the earth."
    for actual in utils.strip_verses(kjv):
        if idx == 1:
            assert actual == expected
            break
        idx += 1
