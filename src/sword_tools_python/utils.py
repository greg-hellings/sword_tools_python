import Sword

mgr = Sword.SWMgr()


def get_mod(module: str) -> Sword.SWModule:
    module = mgr.getModule(module)
    return module


def strip_verses(module: Sword.SWModule) -> str:
    # Create a new key at the start of the module
    key = module.createKey()
    key.setIndex(0)
    module.setKey(key)
    # Until we reach the end of the module, iterate
    while key.popError() == "\x00":
        yield module.stripText()
        key.increment()
        module.setKey(key)
