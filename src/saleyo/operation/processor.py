from inspect import getsource
from types import ModuleType
from typing import Any, Callable, Optional, Type

from ..base.typing import NameSpace
from ..base.toolchain import Container, ToolChain
from ..base.template import MixinOperation


class Processor(MixinOperation[Callable[[str], str]]):
    """
    If you want to get the soure code of a method and use `split` and `replace` to modify and redefine it,Try `Processor`.

    When you try to use this, please make sure you configure the correct module of your target, or you can use `extra_namespace` to supplement the missing things.

    Don't try to use it with external code, like the code of cpython, it will crash.
    """

    module: Optional[ModuleType]
    extra_namespace: Optional[NameSpace]
    target_name: Optional[str]
    prefix_indent: Optional[int]

    def __init__(
        self,
        argument: Callable[[str], str],
        level: int = 1,
        target_name: Optional[str] = None,
        prefix_indent: Optional[int] = None,
        module: Optional[ModuleType] = None,
        extra_namespace: Optional[NameSpace] = None,
    ) -> None:
        super().__init__(argument, level)
        self.target_name = target_name
        self.prefix_indent = prefix_indent
        self.module = module
        self.extra_namespace = extra_namespace

    @staticmethod
    def configure(
        level: int = 1,
        target_name: Optional[str] = None,
        prefix_indent: Optional[int] = None,
        module: Optional[ModuleType] = None,
        extra_namespace: Optional[NameSpace] = None,
    ) -> Callable[[Callable[[str], str]], "Processor"]:
        return lambda argument: Processor(
            argument=argument,
            level=level,
            prefix_indent=prefix_indent,
            target_name=target_name,
            module=module,
            extra_namespace=extra_namespace,
        )

    def mixin(
        self,
        target: Type[Any],
        toolchain: ToolChain = ToolChain(),
    ) -> None:
        target_name = (
            self.target_name if self.target_name is not None else self.argument.__name__
        )

        return toolchain.tool_setattr(
            target,
            target_name,
            Container(
                None if self.module is None else self.module.__dict__,
                self.extra_namespace,
            ).define_function(
                function_name=target_name,
                indent=self.prefix_indent,
                source=self.argument(
                    getsource(
                        toolchain.tool_getattr(
                            target,
                            target_name,
                        )
                    )
                ),
            ),
        )
