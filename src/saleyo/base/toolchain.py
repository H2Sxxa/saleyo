from dataclasses import dataclass
from inspect import signature
from types import FunctionType
from typing import Any, Callable, Dict, Generic, Optional


from ..base.typing import T, NameSpace


@dataclass
class ToolChain:
    """
    The tool to do mixin.

    Default to use `getattr`/`setattr`/`hasattr`
    """

    tool_getattr: Callable[[Any, str], Any] = getattr
    tool_setattr: Callable[[Any, str, Any], None] = setattr
    tool_hasattr: Callable[[Any, str], bool] = hasattr


class Container:
    """
    Container is A Class to keep a namespace and use this namespace to define function / variable / ...
    """

    environment: NameSpace

    def __init__(self, *namespace: Optional[NameSpace]) -> None:
        self.environment = {
            k: v for _ in namespace if _ is not None for k, v in _.items()
        }

    def exec(self, source: str) -> Dict[str, Any]:
        exec(source, self.environment)
        return self.environment

    def define_function(
        self, function_name: str, source: str, indent: Optional[int] = None
    ) -> FunctionType:
        if indent is None:
            indent = len(source[: source.find(source.lstrip()[0])])

        return self.exec(
            source="\n".join(
                [line.removeprefix(" " * indent) for line in source.splitlines()]
            )
        )[function_name]


@dataclass
class InvokeEvent(Generic[T]):
    target: Callable[..., T]
    argument: Dict[str, Any]

    @staticmethod
    def from_call(target: Callable[..., T], *args, **kwargs) -> "InvokeEvent[T]":
        argument = {}
        function_parameters = signature(target).parameters
        arg_names = list(function_parameters.keys())
        argument.update({k: v.default for k, v in function_parameters.items()})
        for arg in args:
            argument[arg_names.pop(0)] = arg
        argument.update(kwargs)
        return InvokeEvent(target=target, argument=argument)

    def invoke(self) -> T:
        return self.target(**self.argument)
