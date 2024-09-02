from typing import Any, Union
from saleyo.decorator.compile import CompileToken, CompileBoundary
import targetmodule


@CompileToken(lambda info: "targetmodule.py" in str(info.filename))
def mixin_a(token: Union[str, bytes, Any]):
    if not isinstance(token, bytes):
        return
    return token.replace(b"static", b"bye2")


with CompileBoundary(no_cache=False) as compile:
    compile.recompile_module(targetmodule)


print(targetmodule.Static().FIELD)  # hello bye
