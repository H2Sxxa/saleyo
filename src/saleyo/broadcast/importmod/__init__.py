from collections import OrderedDict
from types import ModuleType
from typing import Any, Callable, Dict, Optional, Union

from saleyo.base.broadcast import BroadCaster
from saleyo.base.typing import IterableOrSingle, M


class ImportBroadCaster(BroadCaster[[str, ModuleType], IterableOrSingle[M]]):
    _instance: Optional["ImportBroadCaster"] = None
    _initialize_flag: bool = False
    _listeners: OrderedDict[
        Union[str, int], Callable[[str, ModuleType], IterableOrSingle[M]]
    ] = OrderedDict()

    _disposable_listeners: OrderedDict[
        Union[str, int], Callable[[str, ModuleType], IterableOrSingle[M]]
    ] = OrderedDict()

    def listeners(
        self,
        disposable: bool = False,
    ) -> Dict[Any, Callable[[str, ModuleType], IterableOrSingle[M]]]:
        return self._disposable_listeners if disposable else self._listeners

    @staticmethod
    def instance() -> "ImportBroadCaster":
        if not ImportBroadCaster._instance:
            ImportBroadCaster._instance = ImportBroadCaster()
        return ImportBroadCaster._instance

    @staticmethod
    def initialize():
        if ImportBroadCaster._initialize_flag:
            return

        import sys

        class ImportBroadCastDict(type(sys.modules)):
            def __setitem__(self, key: str, value: ModuleType) -> None:
                ImportBroadCaster.instance().all_notifiers()(key, value)

                return super().__setitem__(key, value)

        sys.modules = ImportBroadCastDict(sys.modules)
        ImportBroadCaster._initialize_flag = True
