from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple, Union

_initialize_flag = False


@dataclass
class CompileInfo:
    source: Union[str, bytes, Any]
    filename: Union[str, bytes, Any]
    mode: str
    args: Tuple[Any]
    kwargs: Dict[str, Any]

    def copy(
        self,
        source: Optional[Union[str, bytes, Any]] = None,
        filename: Optional[Union[str, bytes, Any]] = None,
        mode: Optional[str] = None,
        args: Optional[Tuple[Any]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
    ) -> "CompileInfo":
        return CompileInfo(
            source=source if source else self.source,
            filename=filename if filename else self.filename,
            mode=mode if mode else self.mode,
            args=args if args else self.args,
            kwargs=kwargs if kwargs else self.kwargs.copy(),
        )


_listeners: OrderedDict[
    Union[str, int], Callable[[CompileInfo], Optional[CompileInfo]]
] = OrderedDict()

_disposable_listeners: OrderedDict[
    Union[str, int], Callable[[CompileInfo], Optional[CompileInfo]]
] = OrderedDict()


def add_listen_compile(
    listener: Callable[[CompileInfo], Optional[CompileInfo]],
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


def list_compile_listeners(disposable: bool = False):
    return _disposable_listeners if disposable else _listeners


def remove_listen_compile(
    key: Union[str, int, Callable[[CompileInfo], Optional[CompileInfo]]],
    disposable: bool = False,
):
    listeners = _disposable_listeners if disposable else _listeners

    del listeners[key if isinstance(key, str) or isinstance(key, int) else hash(key)]


def initialize_compile_broadcast():
    global _initialize_flag
    if _initialize_flag:
        return

    import builtins

    origin_compile = compile

    def broadcast(
        source: Union[str, bytes, Any],
        filename: Union[str, bytes, Any],
        mode,
        *args,
        **kwargs,
    ):
        info = CompileInfo(source, filename, mode, args, kwargs)
        # BroadCast
        for listener in _listeners.copy().values():
            result = listener(info)
            if result:
                info = result
        # Disposable
        for hashkey, listener in _disposable_listeners.copy().items():
            listener(info)
            result = listener(info)
            if result:
                info = result
            del _disposable_listeners[hashkey]

        return origin_compile(
            info.source,
            info.filename,
            info.mode,
            *info.args,
            **info.kwargs,
        )

    builtins.compile = broadcast

    _initialize_flag = True
