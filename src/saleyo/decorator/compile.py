from typing import Any, Callable, Optional, Union

from saleyo.broadcast.compile import (
    CompileBoundary as CompileBoundary,
)
from saleyo.broadcast.compile import (
    CompileBroadCaster,
    CompileInfo,
)


class CompileTime:
    """
    This decorator is **dangerous**, it will affect the compile of .pyc.
    If you found it not work, please consider delete the target import `__py_cache__`
    and then use a `CompileBoundary`
    """

    locator: Callable[[CompileInfo], bool]
    dispose_key: Any
    key: Optional[Any]
    auto_dispose: bool
    disposable: bool

    def __init__(
        self,
        locator: Callable[[CompileInfo], bool],
        key: Optional[Any] = None,
        initialize: bool = True,
        auto_dispose: bool = True,
        disposable: bool = False,
    ) -> None:
        self.locator = locator
        self.key = key
        self.auto_dispose = auto_dispose
        self.disposable = disposable

        if initialize:
            CompileBroadCaster.instance().initialize()

    def __key_rev(self, key):
        self.dispose_key = key

    def __call__(self, processor: Callable[[CompileInfo], CompileInfo]):
        broadcast = CompileBroadCaster.instance()

        def listener(info: CompileInfo):
            if self.locator(info):
                if self.auto_dispose and self.dispose_key:
                    broadcast.remove_listener(self.dispose_key, self.disposable)

                return processor(info)

        broadcast.add_listener(
            listener=listener,
            key=self.key,
            key_rev=self.__key_rev if self.auto_dispose else None,
            disposable=self.disposable,
        )

        return processor


class CompileToken(CompileTime):
    """
    Alternative version of CompileTime, just modify source.
    But it is also **dangerous**.
    """

    def __call__(
        self, processor: Callable[[Union[str, bytes, Any]], Union[str, bytes, Any]]
    ):
        def wrapper(info: CompileInfo):
            return info.copy(source=processor(info.source))

        return super().__call__(wrapper)
