from saleyo.decorator.file import FileLoadTime


@FileLoadTime(lambda path, bytecode: True)
def mixin(path, bytecode):
    print(path)
    print(bytecode)
    return bytecode


import targetmodule  # noqa: E402, F401
