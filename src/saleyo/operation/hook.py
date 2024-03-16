from typing import Any, Callable, Optional, Type, Union

from ..base.typing import P, RT, T
from ..base.toolchain import ToolChain, Arguments
from ..base.template import MixinOperation


class Post(MixinOperation[Callable[[T], Optional[RT]]]):
    """
    `Post` will call after the target method, and the callable should be decorated as `@staticmethod` and have one argument to receive the result of target method.

    If the `post` function return value is not `None`, it will replace the original result.
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

    def mixin(self, target: Type[Any], toolchain: ToolChain = ToolChain()) -> None:
        target_name = (
            self.target_name if self.target_name is not None else self.argument.__name__
        )
        native_function: Callable[..., T] = toolchain.tool_getattr(target, target_name)

        def post(*args, **kwargs) -> Union[T, RT]:
            result = native_function(*args, **kwargs)
            post_result = self.argument(result)
            if post_result is not None:
                return post_result
            return result

        return toolchain.tool_setattr(target, target_name, post)


class Pre(MixinOperation[Callable[P, Optional[Arguments[P]]]]):
    """
    `Pre` will call before the target method, and the callable should be decorated as `@staticmethod` and have `*args,**kwargs` to receive the arguments of target method.

    If the `pre` function return value is a `Aruguments`(not `None`), it will replace the original arguments.
    """

    target_name: Optional[str]

    def __init__(
        self,
        argument: Callable[P, Optional[Arguments[P]]],
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
        return lambda argument: Pre(
            argument=argument,
            target_name=target_name,
            level=level,
        )

    def mixin(self, target: Type[Any], toolchain: ToolChain = ToolChain()) -> None:
        target_name = (
            self.target_name if self.target_name is not None else self.argument.__name__
        )
        native_function = toolchain.tool_getattr(target, target_name)

        def pre(*args: P.args, **kwargs: P.kwargs) -> Any:
            arguments = self.argument(*args, **kwargs)
            if arguments is not None:
                return native_function(*arguments.args, **arguments.kwargs)
            return native_function(*args, **kwargs)

        return toolchain.tool_setattr(target, target_name, pre)
