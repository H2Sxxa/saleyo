from collections import OrderedDict
from types import ModuleType
from typing import Any, Callable, Optional, Union


_initialize_flag = False

_listeners: OrderedDict[Union[str, int], Callable[[str, ModuleType], Any]] = (
    OrderedDict()
)

_disposable_listeners: OrderedDict[
    Union[str, int], Callable[[str, ModuleType], Any]
] = OrderedDict()


def add_listen_import(
    listener: Callable[[str, ModuleType], Any],
    key: Optional[str] = None,
    disposable: bool = False,
):
    listeners = _disposable_listeners if disposable else _listeners

    hashkey = key if key else hash(listener)
    if hashkey in listeners:
        raise Exception(f"{hashkey} Duplicate!")
    listeners[hashkey] = listener


def remove_listen_import(
    key: Union[str, Callable[[str, ModuleType], Any]],
    disposable: bool = False,
):
    listeners = _disposable_listeners if disposable else _listeners

    del listeners[key if isinstance(key, str) else hash(key)]


def remove_listen_import_hash(
    hash: int,
    disposable: bool = False,
):
    listeners = _disposable_listeners if disposable else _listeners

    del listeners[hash]


def initialize_import_broadcast():
    global _initialize_flag
    if _initialize_flag:
        return

    import sys

    class ImportBroadCastDict(type(sys.modules)):
        def __setitem__(self, key: str, value: ModuleType) -> None:
            # BroadCast
            for listener in _listeners.values():
                listener(key, value)
            # disposable
            for hashkey, listener in _disposable_listeners.items():
                listener(key, value)
                del _disposable_listeners[hashkey]

            return super().__setitem__(key, value)

    sys.modules = ImportBroadCastDict(sys.modules)
    _initialize_flag = True
