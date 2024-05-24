from saleyo import Insert, Mixin
from saleyo.operation.accessor import Accessor, FunctionAccessor


class Foo:
    __value: int = 1

    def __increase_value(self) -> None:
        self.__value += 1

    def get_val(self):
        return self.__value


@Mixin(target=Foo)
class MixinFoo:
    value_accessor: Accessor[int] = Accessor("__value")
    increase_value: FunctionAccessor[[Foo], None] = FunctionAccessor("__increase_value")

    @Insert
    def helloworld(self):
        assert isinstance(self, Foo)
        MixinFoo.value_accessor.value += 1
        MixinFoo.increase_value(self)


foo: MixinFoo = Foo()
foo.helloworld()
assert isinstance(foo, Foo)
print(foo.get_val())
print(MixinFoo.value_accessor)
