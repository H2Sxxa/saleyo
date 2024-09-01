from typing import Any, Union
from saleyo.decorator.compile import CompileToken, CompileBoundary


@CompileToken(lambda info: "targetmodule.py" in str(info.filename))
def mixin_a(token: Union[str, bytes, Any]):
    if not isinstance(token, bytes):
        return
    return token.replace(b"static' tag", b"bye")


with CompileBoundary():
    from targetmodule import StaticMap

print(StaticMap().FIELD)  # hello bye
