from saleyo import Alias, GCToolChain

Alias("upper", "do_upper").mixin(str, GCToolChain)

print("Hello Saleyo!".do_upper())
print("Hello Saleyo!".upper())
