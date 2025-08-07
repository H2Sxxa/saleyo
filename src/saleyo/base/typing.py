from types import ModuleType
from typing import Any, Dict, Iterable, Type, TypeVar, Union

try:
    from typing import ParamSpec
except ImportError:
    try:
        from typing_extensions import ParamSpec  # type: ignore
    except ImportError as e:
        raise ImportError(
            "Please install typing_extensions for Python < 3.10 for ParamSpec."
        ) from e

# Generic

RT = TypeVar("RT")
"""
`RT` means `Return Type`
"""
T = TypeVar("T")
"""
`T` means `Type`
"""
P = ParamSpec("P")
"""
`P` means `Params`
"""

M = TypeVar("M", Type[Any], ModuleType, Any)
"""
These can be the target of mixin.
"""

# Alias

NameSpace = Dict[str, Any]
"""
`NameSpace` is the alias of `Dict[str, Any]`
"""

IterableOrSingle = Union[T, Iterable[T]]
"""
`IterableOrSingle[T]` is the alias of `Union[T, List[T]]` 
"""
