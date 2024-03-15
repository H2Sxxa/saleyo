from types import MethodType
from typing import Callable, Optional, Type
from ..base.toolchain import ToolChain
from ..base.template import MixinOperation


class OverWrite(MixinOperation[MethodType]):
    """
    OverWrite is rude and it will cover the target method.
    """

    target_name: Optional[str]

    def __init__(
        self,
        argument: MethodType,
        target_name: Optional[str] = None,
    ) -> None:
        super().__init__(argument)
        self.target_name = target_name

    @staticmethod
    def configure(
        target_name: Optional[str] = None,
    ) -> Callable[[MethodType], "OverWrite"]:
        return lambda argument: OverWrite(
            argument=argument,
            target_name=target_name,
        )

    def mixin(self, target: Type, toolchain: ToolChain = ToolChain()) -> None:
        target_name = (
            self.argument.__name__ if self.target_name is None else self.target_name
        )
        # self.argument.__qualname__ = f"{target.__name__}.{target_name}"
        return toolchain.tool_setattr(
            target,
            target_name,
            self.argument,
        )
