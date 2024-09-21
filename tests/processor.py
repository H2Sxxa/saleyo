from saleyo import Mixin, Processor, Token


class Target:
    @staticmethod
    def target_func():
        pass


@Mixin(target=Target)
class SelfMix:
    @Processor.configure(target_name="target_func")
    @staticmethod
    def processor(token: str):
        tk = Token(token)
        tk.declearation = ["def target_func(param: str):"]
        tk.code = ["return 'hello world'"]
        print(tk)
        return tk.build()


print(Target().target_func("hello"))  # type: ignore
