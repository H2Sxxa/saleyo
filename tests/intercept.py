from saleyo import Mixin, Intercept, Post, Pre, InvokeEvent


class Foo:
    def demo(self):
        print("goodbye~")


@Mixin(target=Foo)
class MixinFoo:
    @Intercept.configure(target_name="demo")
    @staticmethod
    def intercept_demo(_: InvokeEvent):
        return InvokeEvent(lambda: print("hello world"))

    @Pre.configure(target_name="demo")
    def pre_demo(*arg):
        print("pre hello world")

    @Post.configure(target_name="demo")
    def post_demo(*arg):
        print("post hello world")


Foo().demo()
