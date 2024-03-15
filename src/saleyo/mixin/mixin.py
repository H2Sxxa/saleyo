from typing import List, Type

from ..base.template import MixinOperation
from ..base.toolchain import ToolChain
from ..base.typing import T, Target


class Mixin:
    """
    A `Mixin` Decorator is used to invoke all the `MixinOperation` in Mixin Class
    """

    target_class: List[Type]
    toolchain: ToolChain

    def __init__(
        self,
        target_class: Target,
        toolchain: ToolChain = ToolChain(),
    ) -> None:
        self.target_class = (
            target_class if isinstance(target_class, list) else [target_class]
        )
        self.toolchain = toolchain

    def collect(self, mixin: T) -> T:
        for member in map(
            lambda name: self.toolchain.tool_getattr(mixin, name),
            filter(lambda name: not name.startswith("_"), dir(mixin)),
        ):
            if not isinstance(member, MixinOperation):
                continue
            
            for target in self.target_class:
                member.mixin(target=target, toolchain=self.toolchain)
        return mixin

    def __call__(self, mixin: T) -> T:
        return self.collect(mixin=mixin)
