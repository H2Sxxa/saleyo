from collections import OrderedDict
from types import ModuleType
from typing import Any, Callable, Optional, Union


_initialize_flag = False

_listener: OrderedDict[Union[str, int], Callable[[str, ModuleType], Any]] = (
    OrderedDict()
)


def add_listen_import(
    listener: Callable[[str, ModuleType], Any], key: Optional[str] = None
):
    hashkey = key if key else hash(listener)
    if hashkey in _listener:
        raise Exception(f"{hashkey} Duplicate!")
    _listener[hashkey] = listener


def remove_listen_import(key: Union[str, Callable[[str, ModuleType], Any]]):
    del _listener[key if isinstance(key, str) else hash(key)]


def remove_listen_import_hash(hash: int):
    del _listener[hash]


def initialize_import_broadcast():
    global _initialize_flag
    if _initialize_flag:
        return

    import sys

    class ImportBroadCastDict(type(sys.modules)):
        def __setitem__(self, key: str, value: ModuleType) -> None:
            # BroadCast
            for listener in _listener.values():
                listener(key, value)
            return super().__setitem__(key, value)

    sys.modules = ImportBroadCastDict(sys.modules)
    _initialize_flag = True
