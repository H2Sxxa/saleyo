from typing import Any, Union
from saleyo.decorator.compile import CompileToken, CompileBoundary
import targetmodule


@CompileToken(lambda info: "targetmodule.py" in str(info.filename))
def mixin(token: Union[str, bytes, Any]):
    if not isinstance(token, bytes):
        return
    return token.replace(b"static", b"bye")


CompileBoundary.recompile_module(targetmodule)


print(targetmodule.Static().FIELD)  # hello bye
