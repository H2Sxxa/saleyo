from typing import Any, Callable, Generic, Optional, Type

from ..base.typing import RT, T
from ..base.toolchain import InvokeEvent, ToolChain
from ..base.template import MixinOperation


class Intercept(
    Generic[T, RT], MixinOperation[Callable[[InvokeEvent[T]], InvokeEvent[RT]]]
):
    """
    The `Intercept` allow you to intercept the arguments before invoking target method.

    Then, you can handle these arguments in your own functions.
    """

    target_name: Optional[str]

    def __init__(
        self,
        argument: Callable[[InvokeEvent[T]], InvokeEvent[RT]],
        level: int = 1,
        target_name: Optional[str] = None,
    ) -> None:
        super().__init__(argument, level)
        self.target_name = target_name

    @staticmethod
    def configure(
        level: int = 1,
        target_name: Optional[str] = None,
    ) -> Callable[[Callable[[InvokeEvent[T]], InvokeEvent[RT]]], "Intercept[T, RT]"]:
        return lambda argument: Intercept(
            argument=argument,
            level=level,
            target_name=target_name,
        )

    def mixin(
        self,
        target: Type,
        toolchain: ToolChain = ToolChain(),
    ) -> None:
        target_name = (
            self.target_name if self.target_name is not None else self.argument.__name__
        )
        native_function = toolchain.tool_getattr(
            target,
            target_name,
        )

        def invoke(*args, **kwargs) -> Any:
            return self.argument(
                InvokeEvent.from_call(native_function, *args, **kwargs)
            ).invoke()

        return toolchain.tool_setattr(
            target,
            target_name,
            invoke,
        )
