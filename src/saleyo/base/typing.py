from typing import Any, Dict, Iterable, ParamSpec, TypeVar, Union


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

# Alias

NameSpace = Dict[str, Any]
"""
`NameSpace` is the alias of `Dict[str, Any]`
"""

IterableOrSingle = Union[T, Iterable[T]]
"""
`IterableOrSingle[T]` is the alias of `Union[T, List[T]]` 
"""