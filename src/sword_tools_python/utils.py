"""
Methods to wrap the basic Sword library to be able to do quick and simple
Python style iterations of modules and the like
"""
from typing import Generator

import Sword  # pylint: disable=import-error

mgr = Sword.SWMgr()


def get_mod(module: str) -> Sword.SWModule:
    """
    Simply grabs a module without the need to do more things to configure it
    than this.
    """
    module = mgr.getModule(module)
    return module


def strip_verses(module: Sword.SWModule) -> Generator[str, None, None]:
    """
    A generator to use that iterates verses and yields up the text of the
    verse stripped of formatting and markup.
    """
    # Create a new key at the start of the module
    key = module.createKey()
    key.setIndex(0)
    module.setKey(key)
    # Until we reach the end of the module, iterate
    while key.popError() == "\x00":
        yield module.stripText()
        key.increment()
        module.setKey(key)
