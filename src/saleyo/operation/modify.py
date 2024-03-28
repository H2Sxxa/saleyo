from typing import Any

from ..base.typing import MixinAble
from ..base.toolchain import ToolChain
from ..base.template import MixinOperation


class ReName(MixinOperation[str]):
    """
    Rename the target name.
    """

    new: str

    def __init__(self, old: str, new: str, level=1) -> None:
        super().__init__(old, level)
        self.new = new

    def mixin(self, target: MixinAble, toolchain: ToolChain = ToolChain()) -> None:
        old = toolchain.tool_getattr(target, self.argument)
        toolchain.tool_delattr(target, self.argument)
        return toolchain.tool_setattr(target, self.new, old)


class Del(MixinOperation[str]):
    """
    Delete something named `argument` this from target
    """

    def mixin(self, target: MixinAble, toolchain: ToolChain = ToolChain()) -> None:
        return toolchain.tool_delattr(target, self.argument)


class Alias(MixinOperation[str]):
    """will copy the `argument` attribute to `alias`"""

    alias: str

    def __init__(self, argument: str, alias: str, level=1) -> None:
        super().__init__(argument, level)
        self.alias = alias

    def mixin(self, target: MixinAble, toolchain: ToolChain = ToolChain()) -> None:
        return toolchain.tool_setattr(
            target, self.alias, toolchain.tool_getattr(target, self.argument)
        )


class Insert(MixinOperation[Any]):
    def mixin(self, target: MixinAble, toolchain: ToolChain = ToolChain()) -> None:
        return toolchain.tool_setattr(target, self.argument.__name__, self.argument)
