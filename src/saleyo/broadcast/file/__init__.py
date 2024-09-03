from collections import OrderedDict
from typing import Any, Callable, Dict, Optional, Union

from saleyo.base.broadcast import BroadCaster
from saleyo.base.toolchain import Arguments


class FileLoaderBroadCast(BroadCaster[[str, bytes], Optional[bytes]]):
    _instance: Optional["FileLoaderBroadCast"] = None
    _listeners: OrderedDict[
        Union[str, int], Callable[[str, bytes], Optional[bytes]]
    ] = OrderedDict()

    _disposable_listeners: OrderedDict[
        Union[str, int], Callable[[str, bytes], Optional[bytes]]
    ] = OrderedDict()

    @staticmethod
    def instance() -> "FileLoaderBroadCast":
        if not FileLoaderBroadCast._instance:
            FileLoaderBroadCast._instance = FileLoaderBroadCast()
        return FileLoaderBroadCast._instance

    def listeners(
        self, disposable: bool = False
    ) -> Dict[Any, Callable[[str, bytes], Optional[bytes]]]:
        return self._disposable_listeners if disposable else self._listeners

    @staticmethod
    def initialize():
        from importlib._bootstrap_external import FileLoader

        from saleyo.operation import Both

        instance = FileLoaderBroadCast.instance()

        def get_data(origin: Arguments[FileLoader, str], func):
            bytecode = func(*origin.args, **origin.kwargs)
            arg_path: str = ""

            def on_value(rev: Optional[bytes]):
                if rev:
                    nonlocal bytecode
                    bytecode = rev

            def fix_arguments(self: FileLoader, path: str):
                nonlocal arg_path
                arg_path = path

            fix_arguments(*origin.args, **origin.kwargs)
            instance.all_notifiers(on_value)(arg_path, bytecode)

            return bytecode

        Both(get_data).mixin(FileLoader)
