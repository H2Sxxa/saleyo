from types import ModuleType
from typing import Callable, Generic, Iterable, List, Optional, Union

from saleyo.base.import_broadcast import remove_listen_import

from ..base.template import MixinOperation
from ..base.toolchain import DefaultToolChain, ToolChain
from ..base.typing import IterableOrSingle, M, T


class Mixin(Generic[M]):
    """
    A `Mixin` Decorator is used to invoke all the `MixinOperation` in Mixin Class.

    If the target is a special class, you should custom the toolchain yourself.

    When the target if a `Iterable` object, Please use [`target`]

    It is recommend to use `assert isinstance(self, <target>)` at the head of
    operation functions, although there may be some performance cost,
    but it is worth it in most conditions.

    Allow to have more than one target, but that's not recommended.
    """

    target: Iterable[M]
    toolchain: ToolChain
    reverse_level: bool

    def __init__(
        self,
        target: IterableOrSingle[M],
        toolchain: ToolChain = DefaultToolChain,
        reverse_level: bool = False,
    ) -> None:
        self.target = target if isinstance(target, Iterable) else [target]
        self.toolchain = toolchain
        self.reverse_level = reverse_level

    @staticmethod
    def from_name(
        target: IterableOrSingle[str],
        toolchain: ToolChain = DefaultToolChain,
        reverse_level: bool = False,
        qualname: bool = False,
    ) -> "Mixin":
        """
        Will find target classes via `object.__subclasses__()`.

        If want to find a class named `Foo`, default use the `Foo` to match,
        it will use `module.to.Foo` to match when `qualname` enabled.

        Please use this after the definition of target class.

        The method may takes lots of time when there are a whole lot classes,
        recommand to use `@Mixin()` directly if you can.
        """

        target = target if isinstance(target, Iterable) else [target]

        return Mixin(
            filter(
                lambda clazz: clazz.__name__ in target
                if qualname
                else clazz.__qualname__ in target,
                object.__subclasses__(),
            ),
            toolchain=toolchain,
            reverse_level=reverse_level,
        )

    @staticmethod
    def from_regex(
        pattern: str,
        pattern_flags: int = 0,
        toolchain: ToolChain = DefaultToolChain,
        reverse_level: bool = False,
        qualname: bool = False,
        full_match: bool = False,
    ) -> "Mixin":
        """
        Will use regex pattern to find target classes from the `object.__subclasses__()`

        The `pattern` will convert to a `Pattern[str]` via `re.complie` and
        you can provide flags in `pattern_flags`.

        If want to find a class named `Foo`, default use the `Foo` to match,
        it will use `module.to.Foo` to match when `qualname` enabled.

        Please use this after the definition of target class.

        The method may takes lots of time when there are a whole lot classes,
        recommand to use `@Mixin()` directly if you can.
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

    @staticmethod
    def lazy(
        locator: Callable[[str, ModuleType], Optional[IterableOrSingle[M]]],
        toolchain: ToolChain = DefaultToolChain,
        reverse_level: bool = False,
        key: Optional[str] = None,
        initialize: bool = True,
        auto_dispose: bool = True,
        disposable: bool = False,
    ) -> Callable[[object], Union[int, str]]:
        """
        See `Mixin.lazy_mixin`
        """
        return lambda mixin: Mixin.lazy_mixin(
            mixin,
            locator,
            toolchain,
            reverse_level,
            key,
            initialize,
            auto_dispose,
            disposable,
        )

    @staticmethod
    def lazy_mixin(
        mixin: object,
        locator: Callable[[str, ModuleType], Optional[IterableOrSingle[M]]],
        toolchain: ToolChain = DefaultToolChain,
        reverse_level: bool = False,
        key: Optional[str] = None,
        initialize: bool = True,
        auto_dispose: bool = True,
        disposable: bool = False,
    ) -> Union[int, str]:
        """
        Please call lazy before import a module.

        when the `factory` return a non-None value, the Mixin Class will apply to target.

        You can add the listener yourself to controller more details, please see `saleyo.base.import_broadcast`

        initialize: initialize the import-broadcast

        key: specific the key of listener, you can remove it yourself

        auto_dispose: remove listener after first Mixin

        disposable: remove listener after importing first module
        """
        from saleyo.base.import_broadcast import (
            initialize_import_broadcast,
            add_listen_import,
        )

        if initialize:
            initialize_import_broadcast()

        token = None

        def rev(message):
            nonlocal token
            token = message

        def listener(k, v):
            target = locator(k, v)
            if target:
                Mixin(
                    target=target, toolchain=toolchain, reverse_level=reverse_level
                ).apply_from_class(mixin)
                if token:
                    remove_listen_import(token, disposable=disposable)

        add_listen_import(
            listener,
            key,
            disposable=disposable,
            dispose_token_rev=rev if auto_dispose else None,
        )
        return key if key else hash(listener)

    def apply_from_class(self, mixin: T) -> T:
        """
        Recommand to use it from `@Mixin`
        """
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

    def apply_from_operations(
        self, operations: IterableOrSingle[MixinOperation]
    ) -> None:
        """
        Use operations from a `IterableOrSingle[MixinOperation]` and apply to target.

        Always used to mixin class manually.

        ```python
        mixin = Mixin(...)
        op1 = ...
        op2 = ...
        mixin.apply_from_operations([op1, op2])
        ```
        """
        for operation in (
            operations if isinstance(operations, Iterable) else [operations]
        ):
            for target in self.target:
                operation.mixin(target=target, toolchain=self.toolchain)

    def __call__(self, mixin: T) -> Union[M, T]:
        return self.apply_from_class(mixin=mixin)
