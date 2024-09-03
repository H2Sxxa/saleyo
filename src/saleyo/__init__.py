"""
**Saleyo** is a package to modify external python code in runtime.

`base` module defined some abstract class/type and
you can extend Saleyo by this.

`broadcast` module defines some `BroadCaster`, the broadcaster initialize to inject
functions in builtins/importlib/... and broadcast to support some decorators work.

`decorator` module defines some Decorators, it's the most import module in Saleyo.

`operation` module defines some default `MixinOperation`.

Don't know how to start? Please see the part of Basic Tutorial in README.

The two links below are available.

https://github.com/H2Sxxa/saleyo/blob/main/README.md

https://pypi.org/project/saleyo/
"""

from . import base as base
from . import broadcast as broadcast
from . import decorator as decorator
from . import operation as operation
from .base.template import MixinOperation as MixinOperation
from .base.toolchain import Arguments as Arguments
from .base.toolchain import CPyToolChain as CPyToolChain
from .base.toolchain import GCToolChain as GCToolChain
from .base.toolchain import InvokeEvent as InvokeEvent
from .base.toolchain import ToolChain as ToolChain
from .decorator import Ancestor as Ancestor
from .decorator import CompileTime as CompileTime
from .decorator import CompileToken as CompileToken
from .decorator import FileLoadTime as FileLoadTime
from .decorator import Mixin as Mixin
from .operation import Accessor as Accessor
from .operation import Alias as Alias
from .operation import Both as Both
from .operation import Del as Del
from .operation import FunctionAccessor as FunctionAccessor
from .operation import Insert as Insert
from .operation import Intercept as Intercept
from .operation import OverWrite as OverWrite
from .operation import Post as Post
from .operation import Pre as Pre
from .operation import Processor as Processor
from .operation import ReName as ReName
