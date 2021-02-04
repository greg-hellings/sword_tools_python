"""
Methods to wrap the basic Sword library to be able to do quick and simple
Python style iterations of modules and the like
"""
from typing import Generator

# We disable the lint check on this, because this file is old and supports very
# old versions of Python, and also it needs the underlying C wrapper to work
# properly. And we don't want to have to run binary packages in lint
import Sword  # pylint: disable=import-error

mgr = Sword.SWMgr()


def get_mod(module: str) -> Sword.SWModule:
    """
    Simply grabs a module without the need to do more things to configure it
    than this.
    """
    mod = mgr.getModule(module)
    return mod


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
