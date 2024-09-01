from typing import Any, Union
from saleyo.decorator.compile import CompileToken


@CompileToken(lambda info: "targetmodule.py" in str(info.filename))
def mixin(token: Union[str, bytes, Any]):
    if not isinstance(token, bytes):
        return
    return token.replace(b"static' tag", b"hello world")


import targetmodule  # noqa: E402

print(dir(targetmodule))
print(targetmodule.StaticMap().FIELD)
