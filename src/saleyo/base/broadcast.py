from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Generic, Optional

from saleyo.base.typing import RT, P


class BroadCaster(Generic[P, RT], ABC):
    def add_listener(
        self,
        listener: Callable[P, RT],
        key: Optional[Any] = None,
        key_rev: Optional[Callable[[Any], Any]] = None,
        disposable: bool = False,
    ):
        listeners = self.listeners(disposable)
        hashkey = key if key else hash(listener)
        if hashkey in listeners:
            raise Exception(f"Key: {key} Duplicate.")
        listeners[hashkey] = listener
        if key_rev:
            key_rev(hashkey)

    def remove_listener(self, key: Any, disposable: bool = False):
        listeners = self.listeners(disposable)

        if key not in listeners:
            raise Exception(f"{key} not in listeners.")

        del self.listeners(disposable)[key]

    def notifiers(
        self,
        disposable: bool = False,
        on_value: Optional[Callable[[RT], Any]] = None,
    ) -> Callable[P, None]:
        def notify(*args: P.args, **kwargs: P.kwargs):
            listeners = self.listeners(disposable)
            for key, listener in listeners.copy().items():
                value = listener(*args, **kwargs)
                if value and on_value:
                    on_value(value)

                if disposable:
                    del listeners[key]

        return notify

    def all_notifiers(
        self, on_value: Optional[Callable[[RT], Any]] = None
    ) -> Callable[P, None]:
        def notify(*args: P.args, **kwargs: P.kwargs):
            self.notifiers(False, on_value=on_value)(*args, **kwargs)
            self.notifiers(True, on_value=on_value)(*args, **kwargs)

        return notify

    def notifier(
        self,
        key: Any,
        disposable: bool = False,
        on_value: Optional[Callable[[RT], Any]] = None,
    ) -> Callable[P, None]:
        def notify(*args: P.args, **kwargs: P.kwargs):
            listeners = self.listeners(disposable)
            if key not in listeners:
                raise Exception(f"Cant Find {key} in listeners !")
            value = listeners[key](*args, **kwargs)
            if value and on_value:
                on_value(value)

            if disposable:
                del listeners[key]

        return notify

    @abstractmethod
    def listeners(self, disposable: bool = False) -> Dict[Any, Callable[P, RT]]: ...

    @abstractmethod
    def instance() -> "BroadCaster": ...

    @abstractmethod
    def initialize():
        raise NotImplementedError
