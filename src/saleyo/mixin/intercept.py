from typing import Any, Callable, Type

from ..base.toolchain import InvokeEvent, ToolChain
from ..base.template import MixinOperation


class Intercept(MixinOperation[Callable[[InvokeEvent], InvokeEvent]]):
    """
    The `Intercept` allow you to intercept the arguments before invoking target method.

    Then, you can handle these arguments in your own functions.
    """

    def mixin(
        self,
        target: Type,
        toolchain: ToolChain = ToolChain(),
    ) -> None:
        native_function = toolchain.tool_getattr(
            target,
            self.argument.__name__,
        )

        def invoke(*args, **kwargs) -> Any:
            return self.argument(
                InvokeEvent.from_call(native_function, *args, **kwargs)
            ).invoke()

        return toolchain.tool_setattr(
            target,
            self.argument.__name__,
            invoke,
        )
