from types import ModuleType
from typing import Any

from saleyo.broadcast.importmod import ImportBroadCast
from saleyo.decorator.mixin import Mixin
from saleyo.operation.hook import Pre

broadcast = ImportBroadCast.instance()


def locator(name: str, module: ModuleType):
    if name == "targetmod" and module.__dict__.__contains__("NeedLazyMixin"):
        return module.NeedMixin
    return None


@Mixin.lazy(locator)
class MixinTarget:
    @Pre
    @staticmethod
    def hello(this: Any) -> None:
        print(this)
        print("Pre Hook")


print(broadcast.listeners())
import targetmod  # noqa: E402

print(broadcast.listeners())

targetmod.NeedMixin().hello()
