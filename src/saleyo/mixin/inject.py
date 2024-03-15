from types import MethodType
from typing import Type
from saleyo.base.template import MixinOperation
from saleyo.base.toolchain import ToolChain


class Inject(MixinOperation[MethodType]):
    def mixin(
        self,
        target: Type,
        toolchain: ToolChain = ToolChain(),
    ) -> None:
        return super().mixin(target, toolchain)
