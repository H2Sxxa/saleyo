from typing import Callable, Generic, Optional

from ..base.template import MixinOperation
from ..base.toolchain import DefaultToolChain, ToolChain
from ..base.typing import M, P, T


class Accessor(Generic[T], MixinOperation[str]):
    """
    The Generic `T` is the type of target varible,
    if you want to visit a private function, try to use the subclass `FunctionAccessor`.

    Notice: The value only available after invoking the `mixin` method.

    If the `private` is `True`, will add target class name (like `_Foo`) to the prefix
    to argument, if the target is complex,
    you can set `private` to `False` and provide the true name by yourself.

    Also a variable named `argument` will add to target classes when `private` is `True`

    If you use `@Mixin` and have more than one target classes, the `value` will always
    be the varible of latest target.
    """

    _inner: Optional[T]
    _private: bool

    def __init__(self, argument: str, level=1, private=True) -> None:
        super().__init__(argument, level)
        self._inner = None
        self._private = private

    def mixin(self, target: M, toolchain: ToolChain = DefaultToolChain) -> None:
        self._inner = toolchain.tool_getattr(
            target,
            f"_{target.__name__}{self.argument}" if self._private else self.argument,
        )
        if self._private:
            toolchain.tool_setattr(
                target,
                self.argument,
                self._inner,
            )

    @property
    def value(self) -> T:
        """
        Don't use until The `mixin` method call.
        """
        assert self._inner
        return self._inner

    @value.setter
    def value(self, value: T):
        self._inner = value

    @value.deleter
    def value(self):
        # may cause some problems
        del self.value

    def __str__(self) -> str:
        return f"Accessor {{ value: {self._inner} ({id(self._inner)}) }}"


class FunctionAccessor(Generic[P, T], Accessor[Callable[P, T]]):
    """
    `FunctionAccessor` can be call directly.

    It's recommend to provide the Generic `P` and `T`, it can be useful in `__call__`.

    If the `private` is `True`, will add target class name (like `_Foo`) to the prefix
    to argument, if the target is complex, you can set `private` to `False` and
    provide the true name by yourself.

    Also a variable named `argument` will add to target classes when `private` is `True`

    If you just call in operation functions, you can just use a simple variable with
    `Callable[P, T]` type.

    If you use `@Mixin` and have more than one target classes, the `value` will always
    be the varible of latest target.

    ```python
    something: FunctionAccessor[[str], None] = FunctionAccessor("something")
    ```
    """

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        """
        Call the `argument` function in target, don't use until The `mixin` method call.
        """
        assert self._inner
        return self._inner(*args, **kwargs)
