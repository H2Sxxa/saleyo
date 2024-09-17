from saleyo.broadcast.importmod import ImportBroadCaster
from saleyo.broadcast.importmod import activate as activate

ImportBroadCaster.instance().add_listener(lambda k, v: print(k, v))


def something():
    import targetmod as targetmod


something()
