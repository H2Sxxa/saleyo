from saleyo.base.import_broadcast import activate as activate
from saleyo.base.import_broadcast import add_listen_import

add_listen_import(lambda k, v: print(k, v))


def something():
    import targetmod as targetmod


something()
