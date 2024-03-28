from abc import ABC
from typing import Generic

from .toolchain import ToolChain
from .typing import T, MixinAble


class MixinOperation(Generic[T], ABC):
    """
    The MixinOperation is the base of All Operation.

    The generic `MixinOperation` is the type of argument.

    `level` will affect to the mixin order, default to `1`.
    """

    argument: T
    level: int

    def __init__(self, argument: T, level=1) -> None:
        self.argument = argument
        self.level = level

    def mixin(self, target: MixinAble, toolchain: ToolChain = ToolChain()) -> None:
        raise NotImplementedError(
            f"Not Ready to use this Operation to modify '{target}' via '{toolchain}'"
        )
