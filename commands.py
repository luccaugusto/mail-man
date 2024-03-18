from enum import Enum

class Commands(Enum):
    ADD = '-a'
    REMOVE = '-r'
    TRACK_SINGLE = '-t'
    HELP = '-h'
    HELP_LONG = '--help'
    LIST = '--list'
    TRACK_ALL = '--track-all'
    REMOVE_ALL = '--remove-all'

    @staticmethod
    def show_help():
      print("Usage: mail-man [arg] [tracking code list]")
      print("\t-a tracking-code: add a tracking code to the list")
      print("\t-h: show this help text")
      print("\t-t tracking-code: track a single package")
      print("\t-r tracking-code: remove a package from the list")
      print("\t--help: show this help text")
      print("\t--list: list packages being tracked")
      print("\t--track-all: track all packages from the list")
      print("\t--remove-all: remove all packages from the list")
      exit(1)
