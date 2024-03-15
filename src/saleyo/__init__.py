"""
Saleyo is a module to modify external python code in runtime.

The implements are in `mixin`.

If you want to call the method manually, you can try the `function` module.

If you want to use some decorators, please use the `decorator` module.

The `base` module is used to extend your own `mixin` method.
"""

from . import operation as operation
from . import base as base
from . import mixin as mixin
from .mixin import Mixin as Mixin
