from abc import ABC
from typing import Generic, Type

from .toolchain import ToolChain
from .typing import T


class MixinOperation(Generic[T], ABC):
    """
    The MixinOperation is the base of All Operation.

    The generic `MixinOperation` is the type of argument
    """

    argument: T

    def __init__(self, argument: T) -> None:
        self.argument = argument

    def mixin(self, target: Type, toolchain: ToolChain = ToolChain()) -> None:
        raise NotImplementedError(
            f"Not Ready to use this Operation to modify '{target}' via '{toolchain}'"
        )
