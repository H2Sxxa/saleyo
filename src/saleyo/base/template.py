from abc import ABC
from typing import Any, Generic

from .toolchain import DefaultToolChain, ToolChain
from .typing import M, T


class MixinOperation(Generic[T], ABC):
    """The MixinOperation is the base of All Operation.

    The generic `MixinOperation` is the type of argument.

    `level` will affect to the mixin order, default `1`.

    If you call the `MixinOperation` or call the subclass of this,
    it will call the `MixinOperation.argument`
    """

    argument: T
    level: int

    def __init__(self, argument: T, level: int = 1) -> None:
        self.argument = argument
        self.level = level

    def mixin(self, target: M, toolchain: ToolChain = DefaultToolChain) -> None:
        raise NotImplementedError(
            f"Not Ready to use this Operation to modify '{target}' via '{toolchain}'"
        )

    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...
