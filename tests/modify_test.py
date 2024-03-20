from saleyo import ReName, GCToolChain

ReName("upper", "lower").mixin(str, GCToolChain)

print("Hello Saleyo!".lower())
