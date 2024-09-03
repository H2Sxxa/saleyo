import sys
from collections import OrderedDict
from dataclasses import dataclass
from importlib import reload
from os import unlink
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Dict, Optional, Tuple, Union

from saleyo.base.broadcast import BroadCaster


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


class CompileBroadCast(BroadCaster[[CompileInfo], Optional[CompileInfo]]):
    _instance: Optional["CompileBroadCast"] = None
    _initialize_flag: bool = False
    _listeners: OrderedDict[
        Union[str, int], Callable[[CompileInfo], Optional[CompileInfo]]
    ] = OrderedDict()

    _disposable_listeners: OrderedDict[
        Union[str, int], Callable[[CompileInfo], Optional[CompileInfo]]
    ] = OrderedDict()

    def listeners(
        self,
        disposable: bool = False,
    ) -> Dict[Any, Callable[[CompileInfo], CompileInfo | None]]:
        return self._disposable_listeners if disposable else self._listeners

    @staticmethod
    def instance() -> "CompileBroadCast":
        if not CompileBroadCast._instance:
            CompileBroadCast._instance = CompileBroadCast()
        return CompileBroadCast._instance

    @staticmethod
    def initialize():
        if CompileBroadCast._initialize_flag:
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

            def on_value(rev: Optional[CompileInfo]):
                if rev:
                    nonlocal info
                    info = rev

            CompileBroadCast.instance().all_notifiers(on_value=on_value)(info)

            return origin_compile(
                info.source,
                info.filename,
                info.mode,
                *info.args,
                **info.kwargs,
            )

        builtins.compile = broadcast

        CompileBroadCast._initialize_flag = True


class CompileBoundary:
    """
    Module Inside will force compile.

    ## Example

    ```python
    with CompileBoundary():
        import module_a
        import module_b
        import module_c
    ```
    """

    origin: bool
    no_cache: bool

    def __init__(self, no_cache: bool = True) -> None:
        self.origin = sys.dont_write_bytecode
        self.no_cache = no_cache

    def __enter__(self):
        if self.no_cache:
            self.activate()
        return self

    def __exit__(self, *_):
        if self.no_cache:
            self.deactivate()

    def activate(self):
        sys.dont_write_bytecode = True

    def deactivate(self):
        sys.dont_write_bytecode = self.origin

    @staticmethod
    def recompile_module(module: ModuleType):
        """
        When the module has been loaded before, recompile it to modify

        ## Example

        ```python
        import targetmodule

        # Mixin Here...

        with CompileBoundary(no_cache=False) as compile:
            compile.recompile_module(targetmodule)
        ```
        """
        if hasattr(module, "__cached__"):
            file = Path(module.__cached__)
            if file.exists():
                unlink(module.__cached__)
        reload(module)
