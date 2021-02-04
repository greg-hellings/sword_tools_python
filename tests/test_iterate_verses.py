import pytest
import Sword

from sword_tools_python import utils


@pytest.fixture
def kjv():
    return utils.get_mod("KJV")


def test_kjv_installed():
    keys = [k.c_str() for k in utils.mgr.getModules().keys()]
    assert "KJV" in keys, "Please install the KJV module to SWORD_PATH"


def test_genesis_1_1(kjv):
    idx = 0
    expected = "In the beginning God created the heaven and the earth."
    for actual in utils.strip_verses(kjv):
        print(kjv.getKeyText(), actual)
        if idx == 1:
            assert actual == expected
            break
        idx += 1
