from typing import Any, Type
from saleyo.base.template import MixinOperation
from saleyo.base.toolchain import ToolChain


class Ancestor(MixinOperation[Type[Any]]):
    """
    Ancestor will add the `argument` to `target.__bases__`.
    
    If `reverse`, the `argument` will add to the head of `target.__bases__`.
    
    Don't try to use it with external code and `module`, it may crash.
    """

    reverse: bool

    def __init__(self, argument: Type[Any], level=1, reverse=False) -> None:
        super().__init__(argument, level)
        self.reverse = reverse

    @staticmethod
    def configure(
        level: int = 1,
        reverse=False,
    ):
        return lambda argument: Ancestor(
            argument,
            level=level,
            reverse=reverse,
        )

    def mixin(self, target: Type[Any], toolchain: ToolChain = ToolChain()) -> None:
        return toolchain.tool_setattr(
            target,
            "__bases__",
            (self.argument, *toolchain.tool_getattr(target, "__bases__"))
            if self.reverse
            else (*toolchain.tool_getattr(target, "__bases__"), self.argument),
        )
