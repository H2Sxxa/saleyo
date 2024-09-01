from types import ModuleType
from saleyo.base.import_broadcast import list_import_listeners
from saleyo.decorator.mixin import Mixin
from saleyo.operation.hook import Pre


def locator(name: str, module: ModuleType):
    if name == "targetmod":
        if module.__dict__.__contains__("NeedLazyMixin"):
            return module.NeedLazyMixin
    return None


@Mixin.lazy(locator)
class MixinTarget:
    @Pre
    def hello(self):
        print("Pre Hook")


print(list_import_listeners())
import targetmod as targetmod  # noqa: E402

print(list_import_listeners())

targetmod.NeedLazyMixin().hello()
