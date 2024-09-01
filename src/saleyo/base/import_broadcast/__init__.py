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
    dispose_token_rev: Optional[Callable[[Union[int, str]], Any]] = None,
):
    listeners = _disposable_listeners if disposable else _listeners

    hashkey = key if key else hash(listener)
    if hashkey in listeners:
        raise Exception(f"{hashkey} Duplicate!")

    if dispose_token_rev:
        dispose_token_rev(hashkey)

    listeners[hashkey] = listener


def list_import_listeners(disposable: bool = False):
    return _disposable_listeners if disposable else _listeners


def remove_listen_import(
    key: Union[str, int, Callable[[str, ModuleType], Any]],
    disposable: bool = False,
):
    listeners = _disposable_listeners if disposable else _listeners

    del listeners[key if isinstance(key, str) or isinstance(key, int) else hash(key)]


def initialize_import_broadcast():
    global _initialize_flag
    if _initialize_flag:
        return

    import sys

    class ImportBroadCastDict(type(sys.modules)):
        def __setitem__(self, key: str, value: ModuleType) -> None:
            # BroadCast
            for listener in _listeners.copy().values():
                listener(key, value)
            # Disposable
            for hashkey, listener in _disposable_listeners.copy().items():
                listener(key, value)
                del _disposable_listeners[hashkey]

            return super().__setitem__(key, value)

    sys.modules = ImportBroadCastDict(sys.modules)
    _initialize_flag = True
