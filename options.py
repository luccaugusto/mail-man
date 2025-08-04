from commands import Commands


# TODO: change this to getopts, god why did i decided to do this from scratch???
class Options:
    command: str = Commands.TRACK_ALL.value
    keep_delivered: bool = True
    detailed: bool = False
    code: str = ""
    label: str = ""
    show_delivered: bool = False
    number_of_captchas_to_fetch: int = 0

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

        if Commands.SHOW_DELIVERED.value in args:
            cls.show_delivered = True
            args.remove(Commands.SHOW_DELIVERED.value)

        if Commands.FETCH_CAPTCHAS.value in args:
            cls.fetch_captchas = True
            cls.number_of_captchas_to_fetch = int(args[1]) if len(args) > 1 else 0
            if cls.number_of_captchas_to_fetch <= 0:
                raise ValueError("Number of captchas to fetch must be greater than 0")

        cls.command = args[0] if len(args) > 0 else Commands.TRACK_ALL.value
        cls.code = args[1] if len(args) > 1 else ""
        cls.label = args[2] if len(args) > 2 else ""

        if cls.command == Commands.ADD.value and cls.code == "":
            raise ValueError("Missing Code")


options = Options()
