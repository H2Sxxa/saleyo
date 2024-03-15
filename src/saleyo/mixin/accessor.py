from typing import Generic, Optional, Type

from ..base.toolchain import ToolChain
from ..base.typing import T
from ..base.template import MixinOperation


class Accessor(Generic[T], MixinOperation[str]):
    """
    Want to access and modify some private varibles or methods? Try use `Accessor`!

    Notice: The value only available after invoking the `mixin` method.

    If you use `@Mixin` and have more than one target classes, the `value` will always be the varible of latest target.
    """

    _inner: Optional[T]

    def mixin(self, target: Type, toolchain: ToolChain = ToolChain()) -> None:
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
