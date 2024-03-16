from saleyo.base.toolchain import GCToolChain, InvokeEvent
from saleyo.mixin import Mixin
from saleyo.operation.intercept import Intercept


@Mixin(target=str, toolchain=GCToolChain)
class MixinStr:
    @Intercept.configure(
        target_name="format",
    )
    @staticmethod
    def test(_: InvokeEvent):
        print(_.argument)
        return _


print("HELLO world".format())
