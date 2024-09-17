from saleyo import Processor
from saleyo.decorator.mixin import Mixin
from saleyo.operation.processor import Token


class Target:
    @staticmethod
    def target_func():
        pass


@Mixin(target=Target)
class SelfMix:
    @Processor.configure(target_name="target_func")
    @staticmethod
    def processor(token: str):
        return Token(token.replace("pass", "print('hello world')")).build()


Target().target_func()
