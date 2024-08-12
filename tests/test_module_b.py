import test_module_a
from saleyo.decorator.mixin import Mixin
from saleyo.operation.overwrite import OverWrite


@Mixin(test_module_a)
class MixinModuleA:
    @OverWrite.configure(target_name="hello")
    def hello_over() -> None:
        print("goodbye")

