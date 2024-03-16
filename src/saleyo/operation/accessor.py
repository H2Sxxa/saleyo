from typing import Any, Generic, Optional, Type

from ..base.toolchain import ToolChain
from ..base.typing import T
from ..base.template import MixinOperation


class Accessor(Generic[T], MixinOperation[str]):
    """
    Want to access and modify some private varibles or methods? Try use `Accessor`!

    The Generic is the type of target varible.

    Notice: The value only available after invoking the `mixin` method.

    If you use `@Mixin` and have more than one target classes, the `value` will always be the varible of latest target.
    """

    _inner: Optional[T]

    def __init__(self, argument: str, level=1) -> None:
        super().__init__(argument, level)
        self._inner = None

    @staticmethod
    def configure(level: int = 1):
        return lambda argument: Accessor(
            argument=argument,
            level=level,
        )

    def mixin(self, target: Type[Any], toolchain: ToolChain = ToolChain()) -> None:
        self._inner = toolchain.tool_getattr(
            target,
            f"_{target.__name__}{self.argument}",
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
