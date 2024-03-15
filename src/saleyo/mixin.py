from typing import List, Type

from .base.template import MixinOperation
from .base.toolchain import ToolChain
from .base.typing import T, Target


class Mixin:
    """
    A `Mixin` Decorator is used to invoke all the `MixinOperation` in Mixin Class.
    
    If the target is a special class, you should custom the toolchain yourself.
    
    Allow to have more than one target, but that's not recommended.
    """

    target: List[Type]
    toolchain: ToolChain
    reverse_level: bool

    def __init__(
        self,
        target: Target,
        toolchain: ToolChain = ToolChain(),
        reverse_level: bool = False,
    ) -> None:
        self.target = target if isinstance(target, list) else [target]
        self.toolchain = toolchain
        self.reverse_level = reverse_level

    def collect(self, mixin: T) -> T:
        members: List[MixinOperation] = sorted(
            filter(
                lambda member: isinstance(member, MixinOperation),
                map(
                    lambda name: self.toolchain.tool_getattr(mixin, name),
                    filter(lambda name: not name.startswith("_"), dir(mixin)),
                ),
            ),
            key=lambda member: member.level,
            reverse=self.reverse_level,
        )

        for member in members:
            for target in self.target:
                member.mixin(target=target, toolchain=self.toolchain)
        return mixin

    def __call__(self, mixin: T) -> T:
        return self.collect(mixin=mixin)
