from typing import Any, Iterable, List, Type

from .base.template import MixinOperation
from .base.toolchain import ToolChain
from .base.typing import T, IterableOrSingle


class Mixin:
    """
    A `Mixin` Decorator is used to invoke all the `MixinOperation` in Mixin Class.

    If the target is a special class, you should custom the toolchain yourself.

    Allow to have more than one target, but that's not recommended.
    """

    target: IterableOrSingle[Type[Any]]
    toolchain: ToolChain
    reverse_level: bool

    def __init__(
        self,
        target: IterableOrSingle,
        toolchain: ToolChain = ToolChain(),
        reverse_level: bool = False,
    ) -> None:
        self.target = target if isinstance(target, Iterable) else [target]
        self.toolchain = toolchain
        self.reverse_level = reverse_level

    @staticmethod
    def from_name(
        target: IterableOrSingle[str],
        toolchain: ToolChain = ToolChain(),
        reverse_level: bool = False,
        qualname: bool = False,
    ) -> "Mixin":
        """
        Will find target classes from `object.__subclasses__()` from class name or qualname.

        If want to find a class named `Foo`, default use the `Foo` to match, it will use `module.to.Foo` to match when `qualname` enabled.

        Please use this after the definition of target class.

        The method may takes lots of time when there are a whole lot classes, recommand to use `@Mixin()` directly if you can.
        """

        target = target if isinstance(target, Iterable) else [target]

        return Mixin(
            list(
                filter(
                    lambda clazz: clazz.__name__ in target
                    if qualname
                    else clazz.__qualname__ in target,
                    object.__subclasses__(),
                )
            ),
            toolchain=toolchain,
            reverse_level=reverse_level,
        )

    @staticmethod
    def from_regex(
        pattern: str,
        pattern_flags: int = 0,
        toolchain: ToolChain = ToolChain(),
        reverse_level: bool = False,
        qualname: bool = False,
        full_match: bool = False,
    ) -> "Mixin":
        """
        Will use regex pattern to find target classes from the `object.__subclasses__()`.

        The `pattern` will convert to a `Pattern[str]` via `re.complie` and you can provide flags in `pattern_flags`.

        If want to find a class named `Foo`, default use the `Foo` to match, it will use `module.to.Foo` to match when `qualname` enabled.

        Please use this after the definition of target class.

        The method may takes lots of time when there are a whole lot classes, recommand to use `@Mixin()` directly if you can.
        """
        import re

        regex_pattern = re.compile(pattern=pattern, flags=pattern_flags)
        matcher = regex_pattern.fullmatch if full_match else regex_pattern.match

        return Mixin(
            list(
                filter(
                    lambda clazz: matcher(
                        clazz.__name__ if qualname else clazz.__qualname__
                    )
                    is not None,
                    object.__subclasses__(),
                )
            ),
            toolchain=toolchain,
            reverse_level=reverse_level,
        )

    def collect(self, mixin: T) -> T:
        members: List[MixinOperation] = sorted(
            filter(
                lambda member: isinstance(member, MixinOperation),
                map(
                    lambda name: self.toolchain.tool_getattr(mixin, name),
                    filter(lambda name: not name.startswith("_"), dir(mixin)),
                ),
            ),
            key=lambda member: member.level,
            reverse=self.reverse_level,
        )

        for member in members:
            for target in self.target:
                member.mixin(target=target, toolchain=self.toolchain)
        return mixin

    def __call__(self, mixin: T) -> T:
        return self.collect(mixin=mixin)
