from typing import Any, Callable, Optional, Type

from ..base.toolchain import ToolChain
from ..base.template import MixinOperation


class OverWrite(MixinOperation[Callable]):
    """
    OverWrite is rude and it will cover the target method.

    If the target method doesn't exist, overwrite will add overwrite method to target class.

    Try avoid using `OverWrite` with other `OverWrite`.
    """

    target_name: Optional[str]

    def __init__(
        self,
        argument: Callable,
        target_name: Optional[str] = None,
    ) -> None:
        super().__init__(argument)
        self.target_name = target_name

    @staticmethod
    def configure(
        target_name: Optional[str] = None,
    ) -> Callable[[Callable], "OverWrite"]:
        return lambda argument: OverWrite(
            argument=argument,
            target_name=target_name,
        )

    def mixin(self, target: Type[Any], toolchain: ToolChain = ToolChain()) -> None:
        target_name = (
            self.argument.__name__ if self.target_name is None else self.target_name
        )
        self.argument.__qualname__ = f"{target.__name__}.{target_name}"
        return toolchain.tool_setattr(
            target,
            target_name,
            self.argument,
        )
