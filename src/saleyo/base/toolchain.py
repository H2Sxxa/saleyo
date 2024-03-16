from dataclasses import dataclass
import ctypes as _ctypes
from types import FunctionType
from typing import Any, Callable, Dict, Generic, Optional
from gc import get_referents as _get_referents


from ..base.typing import P, RT, NameSpace


@dataclass
class ToolChain:
    """
    The tool to do mixin.

    Default to use `getattr`/`setattr`/`hasattr`
    """

    tool_getattr: Callable[[Any, str], Any] = getattr
    tool_setattr: Callable[[Any, str, Any], None] = setattr
    tool_hasattr: Callable[[Any, str], bool] = hasattr


GCToolChain = ToolChain(
    tool_getattr=lambda _object, _name: _get_referents(_object.__dict__)[0][_name],
    tool_hasattr=lambda _object, _name: _name in _get_referents(_object.__dict__)[0],
    tool_setattr=lambda _object, _name, _attr: _get_referents(_object.__dict__)[
        0
    ].update({_name: _attr}),
)
"""
GC ToolChain use the `get_referents` functions in `gc` and it can modify some special class.

Notice: There is no guarantee that it can modify any class, and this method is rude and danger, avoid using it in produce environment.
"""


def _cpy_get_dict(_object: Any) -> Dict[str, Any]:
    return _ctypes.cast(
        id(_object) + type(_object).__dictoffset__, _ctypes.POINTER(_ctypes.py_object)
    ).contents.value


CPyToolChain = ToolChain(
    tool_getattr=lambda _object, _name: _cpy_get_dict(_object)[_name],
    tool_hasattr=lambda _object, _name: _name in _cpy_get_dict(_object),
    tool_setattr=lambda _object, _name, _attr: _cpy_get_dict(_object).update(
        {_name: _attr}
    ),
)
"""
`CPyToolChain` use the `ctypes` to modify class, it's danger than other default toolchains.

Notice: There is no guarantee that it can modify any class, and this method is rude and danger, avoid using it in produce environment.
"""


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


class Arugument(Generic[P]):
    """
    `Argument` is used to call function, the Generic `P` is the params of target function.
    """

    def __init__(self, *args: P.args, **kwargs: P.kwargs) -> None:
        self.positional = args
        self.keyword = kwargs

    def __str__(self) -> str:
        return f"Arugument(positional: {self.positional}, keyword: {self.keyword} )"


@dataclass
class InvokeEvent(Generic[P, RT]):
    """
    A `InvokeEvent` includes the target function and the arguments to call this functions.

    Recommend to use the static method `InvokeEvent.from_call` to get a `InvokeEvent`.
    """

    target: Callable[P, RT]
    argument: Arugument[P]

    @staticmethod
    def from_call(
        target: Callable[P, RT],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> "InvokeEvent[P, RT]":
        return InvokeEvent(
            target=target,
            argument=Arugument(
                *args,
                **kwargs,
            ),
        )

    def invoke(self, target: Callable[P, RT]) -> RT:
        return target(*self.argument.positional, **self.argument.keyword)

    def invoke_target(self) -> RT:
        return self.target(*self.argument.positional, **self.argument.keyword)
