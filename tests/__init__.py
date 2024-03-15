from saleyo.base.toolchain import InvokeEvent
from saleyo.mixin import Mixin
from saleyo.mixin.intercept import Intercept


class Foo:
    def demo(self, hello, bad=0):
        print("goodbye~")


@Mixin(target_class=Foo)
class A:
    @Intercept
    @staticmethod
    def demo(_: InvokeEvent[None]):
        return InvokeEvent.from_call(lambda: print("hello world"))


Foo().demo(1)
