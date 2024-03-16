from saleyo import Mixin, GCToolChain, Arguments, Pre


@Mixin(target=str, toolchain=GCToolChain)
class MixinStr:
    @Pre.configure(target_name="format")
    def pre_format(self, *args) -> Arguments[...]:
        print(f"input args: {args}")
        return Arguments(self, "python")


print("hello world {}".format("saleyo"))
