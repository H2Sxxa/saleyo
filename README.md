# Saleyo

Saleyo is a lightwight scalable Python AOP framework, easy to use and integrate.

## Getting Start

```sh
pip install saleyo
```

## Basic Tutorial

### Declear a `Mixin` class

If you don't like decorators, you can pass arguments to operations and call the `mixin` method manually.

```python
from saleyo import Mixin

class Foo:...


@Mixin(target = Foo)
class MixinFoo:...
```

### Use `MixinOperation`

Here is a simple demo.

```python
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

>>> private varible
>>> hello saleyo
>>> pre hello world
>>> hello world
>>> post hello world
```

### Custom ToolChain

`ToolChain` determines the ability to modify the class.

```python
from saleyo import Mixin, GCToolChain, Arguments, Pre


@Mixin(target=str, toolchain=GCToolChain)
class MixinStr:
    @Pre.configure(target_name="format")
    def pre_format(self, *args) -> Arguments[...]:
        print(f"input args: {args}")
        return Arguments(self, "saleyo")


print("hello world {}".format("python"))

>>> input args: ('python',)
>>> hello world saleyo
```


### Custom Operation

The default operations can't satify you? Why not try define a operation yourself!

```python
from typing import Any, Type
from saleyo import MixinOperation, ToolChain

class MyOperation(MixinOperation[Any]):
    def mixin(self, target: Type, toolchain: ToolChain = ...) -> None:
        ...
```

