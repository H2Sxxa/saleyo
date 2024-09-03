from typing import Any, Union

import targetmodule

from saleyo.decorator.compile import CompileBoundary, CompileToken


@CompileToken(lambda info: "targetmodule.py" in str(info.filename))
def mixin(token: Union[str, bytes, Any]):
    if not isinstance(token, bytes):
        return
    return token.replace(b"static", b"bye")


CompileBoundary.recompile_module(targetmodule)


print(targetmodule.Static().FIELD)  # hello bye
