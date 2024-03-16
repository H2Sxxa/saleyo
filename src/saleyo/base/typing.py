from typing import Any, Dict, List, ParamSpec, Type, TypeVar, Union

Target = Union[Type[Any], List[Type[Any]]]
"""
`Target` is the target of `@Mixin`, it's the alias of `Union[Type[Any], List[Type[Any]]]`
"""
NameSpace = Dict[str, Any]
"""
`NameSpace` is the alias of `Dict[str, Any]`
"""
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
