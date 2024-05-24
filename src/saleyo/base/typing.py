from types import ModuleType
from typing import Any, Dict, Iterable, ParamSpec, Type, TypeVar, Union

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
