from typing import Any, Callable, Optional

from saleyo.broadcast.file import FileLoaderBroadCast


class FileLoadTime:
    """
    Get SourceCode(.py) / ByteCode(.pyc) from Module Loader and Modify it.

    Please use some third-party packages to modify it.

    When the target module has no cache, it has the same effects to `CompileToken`
    """

    locator: Callable[[str, bytes], bool]
    dispose_key: Any
    key: Optional[Any]
    auto_dispose: bool
    disposable: bool

    def __init__(
        self,
        locator: Callable[[str, bytes], bool],
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
            FileLoaderBroadCast.instance().initialize()

    def key_rev(self, key):
        self.dispose_key = key

    def __call__(self, processor: Callable[[str, bytes], bytes]) -> Any:
        broadcast = FileLoaderBroadCast.instance()

        def listener(path: str, bytecode: bytes):
            if self.locator(path, bytecode):
                if self.auto_dispose and self.dispose_key:
                    broadcast.remove_listener(self.dispose_key, self.disposable)

                return processor(path, bytecode)

        broadcast.add_listener(
            listener=listener,
            key=self.key,
            key_rev=self.key_rev if self.auto_dispose else None,
            disposable=self.disposable,
        )

        return processor
