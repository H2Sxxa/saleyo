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


@Mixin(target = Foo)
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

#### Lazy Mixin - Mixin a Object before importing its module

Lazy Mixin will be triggered after importing

You dont need to care how to import target module, just define a `locator`! 

```python
# targetmod
class NeedMixin:
    def hello(self):
        print("hello world")


# mixin
# put mixin in a single file and import to use is better
from types import ModuleType
from saleyo.base.import_broadcast import list_import_listeners
from saleyo.decorator.mixin import Mixin
from saleyo.operation.hook import Pre


def locater(name: str, module: ModuleType):
    if name == "targetmod":
        if module.__dict__.__contains__("NeedMixin"):
            return module.NeedMixin
    return None # Dont Mixin this module


@Mixin.lazy(locater)
class MixinTarget:
    @Pre
    def hello(self):
        print("Pre Hook")


print(list_import_listeners()) # {hashkey: Callable}
import targetmod as targetmod  # noqa: E402

print(list_import_listeners()) # {} auto dispose after setting

targetmod.NeedMixin().hello()

>>> Pre Hook
>>> hello world
```

#### Operate Compile

Remember clean the target cache before mixin.

```python
# targetmodule
def generate(name):
    return name + " hell world"


class StaticMap:
    FIELD = generate("hello")

# mixin
from typing import Any, Union
from saleyo.decorator.compile import CompileToken


@CompileToken(lambda info: "targetmodule.py" in str(info.filename))
def mixin(token: Union[str, bytes, Any]):
    if not isinstance(token, bytes):
        return
    return token.replace(b"hell world", b"hello world")


import targetmodule  # noqa: E402

print(targetmodule.StaticMap().FIELD)

>>> hello hello world
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
from typing import Any
from saleyo import MixinOperation, ToolChain
from saleyo.base.typing import M

class MyOperation(MixinOperation[Any]):
    def mixin(self, target: M, toolchain: ToolChain = ...) -> None:
        ...
```

