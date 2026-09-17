from enum import Enum
from ui_display import Colors


class Commands(Enum):
    ADD = "-a"
    REMOVE = "-r"
    TRACK_SINGLE = "-t"
    HELP = "-h"
    HELP_LONG = "--help"
    LIST = "--list"
    TRACK_ALL = "--track-all"
    REMOVE_ALL = "--remove-all"
    KEEP = "--keep"
    NO_KEEP = "--no-keep"
    LIST_ALL = "--list-all"
    DETAILED = "--detailed"
    SHOW_DELIVERED = "--show-delivered"
    FETCH_CAPTCHAS = "--fetch-captchas"

    @staticmethod
    def show_help() -> None:
        b = Colors.BOLD
        e = Colors.END
        print(
            f"""{b}Usage:{e} mail-man [command] [arguments] [options]

Track your Correios packages from the terminal.
With no command, every package in the list is tracked.

{b}Commands:{e}
  -a <code> [label]       Add a tracking code to the list
  -r <code>               Remove a package from the list
  -t <code>               Track a single package
  --list                  List the packages being tracked
  --list-all              List tracked and delivered packages
  --track-all             Track every package in the list (default)
  --remove-all            Remove every package from the list
  --fetch-captchas <n>    Download n captchas from the server
  -h, --help              Show this help text

{b}Options:{e}
  --keep                  Keep delivered packages in the list (default)
  --no-keep               Drop delivered packages after tracking
  --show-delivered        Include delivered packages when tracking
  --detailed              Show the full event history

{b}Examples:{e}
  mail-man -a AB123456789BR keyboard
  mail-man -t AB123456789BR
  mail-man --track-all --show-delivered
"""
        )
        exit(1)
