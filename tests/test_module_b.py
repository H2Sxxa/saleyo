from saleyo.mixin import Mixin
from saleyo.operation.overwrite import OverWrite
import test_module_a


@Mixin(test_module_a)
class MixinModuleA:
    @OverWrite.configure(target_name="hello")
    def hello_over():
        print("goodbye")

