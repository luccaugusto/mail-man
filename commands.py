from enum import Enum


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

    @staticmethod
    def show_help() -> None:
        print("Usage: mail-man [arg] [tracking code list]")
        print("\t-a tracking-code: add a tracking code to the list")
        print("\t-h: show this help text")
        print("\t-t tracking-code: track a single package")
        print("\t-r tracking-code: remove a package from the list")
        print("\t--keep: do not delete delivered packages from the list (default)")
        print("\t--no-keep: delete delivered packages from the list")
        print("\t--help: show this help text")
        print("\t--list: list packages being tracked")
        print("\t--list-all: list tracked and delivered packages")
        print("\t--show-delivered: show delivered packages when tracking packages")
        print("\t--track-all: track all packages from the list")
        print("\t--remove-all: remove all packages from the list")
        exit(1)
