from saleyo import Alias, GCToolChain, Mixin

alias = Alias("upper", "do_upper")

Mixin(str, GCToolChain).apply_from_operations(alias)

print("Hello Saleyo!".do_upper()) # type: ignore
print("Hello Saleyo!".upper())
