from typing import Any, Callable, Optional, Union

from saleyo.base.compile_broadcast import (
    CompileInfo,
    add_listen_compile,
    initialize_compile_broadcast,
    remove_listen_compile,
)


class CompileTime:
    """This decorator should be **dangerous**, it will affect the compile of .pyc. If you found it not work, please delete the target import cache"""

    locator: Callable[[CompileInfo], bool]
    token: Union[int, str]
    key: Optional[str]
    auto_dispose: bool
    disposable: bool

    def __init__(
        self,
        locator: Callable[[CompileInfo], bool],
        key: Optional[str] = None,
        initialize: bool = True,
        auto_dispose: bool = True,
        disposable: bool = False,
    ) -> None:
        self.locator = locator
        self.key = key
        self.auto_dispose = auto_dispose
        self.disposable = disposable

        if initialize:
            initialize_compile_broadcast()

    def token_rev(self, token):
        self.token = token

    def __call__(self, processor: Callable[[CompileInfo], CompileInfo]):
        def listener(info: CompileInfo):
            if self.locator(info):
                if self.auto_dispose and self.token:
                    remove_listen_compile(self.token, self.disposable)

                return processor(info)

        add_listen_compile(
            listener=listener,
            key=self.key,
            disposable=self.disposable,
            dispose_token_rev=self.token_rev if self.auto_dispose else None,
        )

        return processor


class CompileToken(CompileTime):
    """Alternative version of CompileTime, just modify source."""

    def __call__(
        self, processor: Callable[[Union[str, bytes, Any]], Union[str, bytes, Any]]
    ):
        def wrapper(info: CompileInfo):
            return info.copy(source=processor(info.source))

        return super().__call__(wrapper)
