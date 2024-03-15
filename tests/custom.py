from typing import Any, Type
from saleyo.base.template import MixinOperation
from saleyo.base.toolchain import ToolChain

class MyOperation(MixinOperation[Any]):
    def mixin(self, target: Type, toolchain: ToolChain = ...) -> None:
        ...