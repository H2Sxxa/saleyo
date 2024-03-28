from typing import Generic, Optional

from ..base.toolchain import ToolChain
from ..base.typing import T, MixinAble
from ..base.template import MixinOperation


class Accessor(Generic[T], MixinOperation[str]):
    """
    Want to access and modify some private varibles or methods? Try use `Accessor`!

    The Generic is the type of target varible.

    Notice: The value only available after invoking the `mixin` method.

    If the `private` is `True`, will add target class name (like `_Foo`) to the prefix to argument.

    If you use `@Mixin` and have more than one target classes, the `value` will always be the varible of latest target.
    """

    _inner: Optional[T]
    _private: bool

    def __init__(self, argument: str, level=1, private=True) -> None:
        super().__init__(argument, level)
        self._inner = None
        self._private = private

    @staticmethod
    def configure(level: int = 1):
        return lambda argument: Accessor(
            argument=argument,
            level=level,
            private=True,
        )

    def mixin(self, target: MixinAble, toolchain: ToolChain = ToolChain()) -> None:
        self._inner = toolchain.tool_getattr(
            target,
            f"_{target.__name__}{self.argument}" if self._private else self.argument,
        )
        return toolchain.tool_setattr(
            target,
            self.argument,
            self._inner,
        )

    @property
    def value(self) -> Optional[T]:
        """
        Will be None Call Before The `mixin` method call.
        """
        return self._inner
