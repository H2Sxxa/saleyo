from ..base.toolchain import InvokeEvent, ToolChain
from ..base.template import MixinOperation

from typing import Any, Callable, Generic, Optional, ParamSpec, Type

_PA = ParamSpec("_PA")
_PB = ParamSpec("_PB")
_A = InvokeEvent[_PA, Any]
_B = InvokeEvent[_PB, Any]


class Intercept(Generic[_PA, _PB], MixinOperation[Callable[[_A[_PA]], _B[_PB]]]):
    """
    The `Intercept` allow you to intercept the arguments before invoking target method.

    Then, you can handle these arguments in your own function and make a redirect to another function.

    If you just want to modify the arguments or the result, please see `Pre` and `Post`.
    """

    target_name: Optional[str]

    def __init__(
        self,
        argument: Callable[[_A[_PA]], _B[_PB]],
        level: int = 1,
        target_name: Optional[str] = None,
    ) -> None:
        super().__init__(argument, level)
        self.target_name = target_name

    @staticmethod
    def configure(
        level: int = 1,
        target_name: Optional[str] = None,
    ) -> Callable[[Callable[[_A[_PA]], _B[_PB]]], "Intercept[_PA, _PB]"]:
        return lambda argument: Intercept(
            argument=argument,
            level=level,
            target_name=target_name,
        )

    def mixin(
        self,
        target: Type[Any],
        toolchain: ToolChain = ToolChain(),
    ) -> None:
        target_name = (
            self.target_name if self.target_name is not None else self.argument.__name__
        )

        native_function = toolchain.tool_getattr(
            target,
            target_name,
        )

        return toolchain.tool_setattr(
            target,
            target_name,
            lambda *args, **kwargs: self.argument(
                InvokeEvent(native_function, *args, **kwargs)
            ).invoke_target(),
        )
