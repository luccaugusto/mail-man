from commands import Commands


class Options:
    command: str = Commands.TRACK_ALL.value
    keep_delivered: bool = True
    detailed: bool = False
    code: str = ""
    label: str = ""

    @classmethod
    def parse_opts(cls, args: list) -> None:
        if Commands.KEEP.value in args:
            cls.keep_delivered = True
            args.remove(Commands.KEEP.value)

        if Commands.NO_KEEP.value in args:
            cls.keep_delivered = False
            args.remove(Commands.NO_KEEP.value)

        if Commands.DETAILED.value in args:
            cls.detailed = True
            args.remove(Commands.DETAILED.value)

        cls.command = args[0] if len(args) > 0 else Commands.TRACK_ALL.value
        cls.code = args[1] if len(args) > 1 else ""
        cls.label = args[2] if len(args) > 2 else ""

        if cls.command == Commands.ADD.value and cls.code == "":
            raise ValueError("Missing Code")


options = Options()
