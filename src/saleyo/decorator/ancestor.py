from typing import Any, Generic, Type

from ..base.toolchain import DefaultToolChain, ToolChain
from ..base.typing import T


class Ancestor(Generic[T]):
    """
    Ancestor will add the `ancestor_class` to `target.__bases__`.
    (Please see `__call__` method)

    Please ensure the `target.__bases__` is not `(object,)`, this decorator requires
    the target has at least one super class.

    If `reverse`, the `argument` will add to the head of `target.__bases__`.

    Don't try to use it with external code and `module`, it will crash.
    """

    reverse: bool
    target: Type[Any]
    toolchain: ToolChain

    def __init__(
        self, target: Type[Any], toolchain: ToolChain = DefaultToolChain, reverse=False
    ) -> None:
        self.reverse = reverse
        self.target = target
        self.toolchain = toolchain

    def __call__(self, ancestor_class: Type[T]) -> Type[T]:
        assert self.target.__bases__ != (object,)

        self.toolchain.tool_setattr(
            self.target,
            "__bases__",
            (ancestor_class, *self.toolchain.tool_getattr(self.target, "__bases__"))
            if self.reverse
            else (
                *self.toolchain.tool_getattr(self.target, "__bases__"),
                ancestor_class,
            ),
        )

        return ancestor_class
