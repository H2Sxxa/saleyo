from saleyo import Ancestor


class _A:
    pass


class A(_A):
    pass


@Ancestor(A)
class AnsA:
    def hello(self):
        print("Hello world!")


a: AnsA = A()
a.hello()
