from typing import Any
from saleyo import Mixin, Accessor, OverWrite, Post, Pre, Intercept, InvokeEvent


class Foo:
    __private = "private varible"

    def demo(self):
        pass


@Mixin(target=Foo)
class MixinFoo:
    # Will add a varible named `__private` to Foo and it has the same address with `_Foo__private`
    private: Accessor[str] = Accessor("__private")

    # Will Add the `func` to `Foo`
    @OverWrite
    def func(self):
        print("hello saleyo")

    # Will intercept the demo method and redirect to `lambda: print("hello world")`
    @Intercept.configure(target_name="demo")
    @staticmethod
    def intercept_demo(_: InvokeEvent):
        return InvokeEvent(lambda: print("hello world"))

    # Will call before `demo` call
    @Pre.configure(target_name="demo")
    def pre_demo(*arg):
        print("pre hello world")

    # Will call after `demo` call
    @Post.configure(target_name="demo")
    def post_demo(*arg):
        print("post hello world")


foo: Any = (
    Foo()
)  # Add the typing hint to avoid the error message from some IDE plugins.

print(foo.__private)  # Also `print(MixinFoo.private.value)`
foo.func()
foo.demo()
