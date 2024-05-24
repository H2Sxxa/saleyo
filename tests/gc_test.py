from saleyo import Arguments, GCToolChain, Mixin, Pre


@Mixin(target=str, toolchain=GCToolChain)
class MixinStr:
    @Pre.configure(target_name="format")
    def pre_format(self, *args, **kwargs) -> Arguments[...]:
        print(f"input args: {args}")
        print(f"input kwargs: {kwargs}")
        return Arguments(self, *args, **kwargs)


print("hello world {},{}".format("saleyo", "some"))
