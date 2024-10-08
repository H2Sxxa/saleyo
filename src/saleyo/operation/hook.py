from typing import Any, Callable, Generic, Optional, Union

from ..base.template import MixinOperation
from ..base.toolchain import Arguments, DefaultToolChain, ToolChain
from ..base.typing import RT, M, P, T


class Post(MixinOperation[Callable[[T], Optional[RT]]]):
    """
    `Post` will call after the target method, and the callable should be decorated as
    `@staticmethod` and have one argument to receive the result of target method.

    If the `post` function return value is not `None`,
    it will replace the original result.
    """

    target_name: Optional[str]

    def __init__(
        self,
        argument: Callable[[T], Optional[RT]],
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

    def mixin(self, target: M, toolchain: ToolChain = DefaultToolChain) -> None:
        target_name = (
            self.target_name if self.target_name is not None else self.argument.__name__
        )
        original_function: Callable[..., T] = toolchain.tool_getattr(
            target, target_name
        )

        def post(*args, **kwargs) -> Union[T, RT]:
            result = original_function(*args, **kwargs)
            post_result = self.argument(result)
            if post_result is not None:
                return post_result
            return result

        return toolchain.tool_setattr(target, target_name, post)


class Pre(Generic[P], MixinOperation[Callable[P, Optional[Arguments[P]]]]):
    """
    `Pre` will call before the target method, and the callable should be decorated as
    `@staticmethod` and have `*args,**kwargs` to receive the arguments of target method.

    If the `pre` function return value is a `Aruguments`(not `None`),
    it will replace the original arguments.
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

    def mixin(self, target: M, toolchain: ToolChain = DefaultToolChain) -> None:
        target_name = (
            self.target_name if self.target_name is not None else self.argument.__name__
        )
        original_function = toolchain.tool_getattr(target, target_name)

        def pre(*args: P.args, **kwargs: P.kwargs) -> Any:
            arguments = self.argument(*args, **kwargs)
            if arguments is not None:
                return original_function(*arguments.args, **arguments.kwargs)
            return original_function(*args, **kwargs)

        return toolchain.tool_setattr(target, target_name, pre)


class Both(
    Generic[P, RT],
    MixinOperation[Callable[[Arguments[P], Callable[P, RT]], RT]],
):
    """
    `Both` will call before the target method, and the callable should be decorated as
    `@staticmethod` and have `*args,**kwargs` to receive the arguments of target method.

    `Both` will give you the original target method and the arguments.
    """

    target_name: Optional[str]

    def __init__(
        self,
        argument: Callable[[Arguments[P], Callable[P, RT]], RT],
        target_name: Optional[str] = None,
        level: int = 1,
    ) -> None:
        super().__init__(argument, level)
        self.target_name = target_name

    def mixin(self, target: M, toolchain: ToolChain = DefaultToolChain) -> None:
        target_name = (
            self.target_name if self.target_name is not None else self.argument.__name__
        )
        original_function = toolchain.tool_getattr(target, target_name)

        def both(*args: P.args, **kwargs: P.kwargs) -> RT:
            return self.argument(Arguments(*args, **kwargs), original_function)

        return toolchain.tool_setattr(target, target_name, both)
