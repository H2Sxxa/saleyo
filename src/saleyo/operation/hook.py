from typing import Callable, Optional, Type

from ..base.typing import RT, T
from ..base.toolchain import ToolChain
from ..base.template import MixinOperation


class Post(MixinOperation[Callable[[T], RT]]):
    """
    `Post` will call after the target method, and the callable should be decorated as `@staticmethod` and have one argument to receive the result of target method.
    """

    target_name: Optional[str]

    def __init__(
        self,
        argument: Callable[[T], RT],
        target_name: Optional[str] = None,
        level: int = 1,
    ) -> None:
        super().__init__(argument, level)
        self.target_name = target_name

    @staticmethod
    def configure(
        level: int = 1,
        target_name: Optional[str] = None,
    ):
        return lambda argument: Post(
            argument=argument,
            target_name=target_name,
            level=level,
        )

    def mixin(self, target: Type, toolchain: ToolChain = ToolChain()) -> None:
        target_name = (
            self.target_name if self.target_name is not None else self.argument.__name__
        )
        native_function = toolchain.tool_getattr(target, target_name)

        def post(*args, **kwargs):
            result = native_function(*args, **kwargs)
            self.argument(result)
            return result

        return toolchain.tool_setattr(target, target_name, post)


class Pre(MixinOperation[Callable[..., RT]]):
    """
    `Pre` will call before the target method, and the callable should be decorated as `@staticmethod` and have `*args,**kwargs` to receive the arguments of target method.
    """
    target_name: Optional[str]

    def __init__(
        self,
        argument: Callable[[T], RT],
        target_name: Optional[str] = None,
        level: int = 1,
    ) -> None:
        super().__init__(argument, level)
        self.target_name = target_name

    @staticmethod
    def configure(
        level: int = 1,
        target_name: Optional[str] = None,
    ):
        return lambda argument: Post(
            argument=argument,
            target_name=target_name,
            level=level,
        )

    def mixin(self, target: Type, toolchain: ToolChain = ToolChain()) -> None:
        target_name = (
            self.target_name if self.target_name is not None else self.argument.__name__
        )
        native_function = toolchain.tool_getattr(target, target_name)

        def pre(*args, **kwargs):
            self.argument(*args, **kwargs)
            result = native_function(*args, **kwargs)
            return result

        return toolchain.tool_setattr(target, target_name, pre)
