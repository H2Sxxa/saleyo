from typing import Any, Dict, List, ParamSpec, Type, TypeVar, Union

Target = Union[Type, List[Type]]
NameSpace = Dict[str, Any]
RT = TypeVar("RT")
T = TypeVar("T")
P = ParamSpec("P")
