from saleyo import Mixin, Insert, ReName


class Foo:
    def hello(self):
        print("hello world")


@Mixin(target=Foo)
class MixinFoo:
    goodbye = ReName("hello", "goodbye")

    @Insert
    def helloworld(self):  # type: ignore
        self.goodbye()


foo: MixinFoo = Foo()
foo.helloworld()
