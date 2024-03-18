#!/bin/python3
import sys
from package_manager import PackageManager, Package
from track_bot import TrackBot
from commands import Commands

def track_all(package_manager: PackageManager):
    print('Tracking all packages')
    print('[', ', '.join([str(c) for c in package_manager.package_list]), ']')

    track_bot = TrackBot()
    statuses = track_bot.track(package_manager.package_list)

    package_manager.assign_statuses(statuses)
    package_manager.show_package_statuses()
    package_manager.remove_delivered(statuses)

def track_single(code):
    print('Tracking package: ', code)
    track_bot = TrackBot()
    package = Package(code)
    status = track_bot.track_single(package.code)
    package_status = next(s for s in status['transito'] if s['cod_objeto_'] == package.code)
    if package_status == None:
        package_status = next(s for s in status['entregue'] if s['cod_objeto_'] == package.code)

    package.set_status(package_status)
    package_manager.show_single_package_status(package)

if __name__ == '__main__':
    args = sys.argv[1:]

    command = args[0] if len(args) > 0 else Commands.TRACK_ALL.value
    code = args[1] if len(args) > 1 else None
    label = args[2] if len(args) > 2 else ''

    try:
        package_manager = PackageManager()

        if command == Commands.ADD.value:
            package_manager.add_package(code, label=label if len(args) > 2 else None)

        elif command == Commands.HELP.value:
            Commands.show_help()

        elif command == Commands.TRACK_SINGLE.value:
            track_single(code)

        elif command == Commands.REMOVE.value:
            package_manager.remove_package(code)

        elif command == Commands.LIST.value:
            package_manager.show_packages()

        elif command == Commands.TRACK_ALL.value:
            track_all(package_manager)

        elif command == Commands.REMOVE_ALL.value:
            package_manager.drop_package_list()

        elif command == Commands.HELP_LONG.value:
            Commands.show_help()
        else:
            Commands.show_help()

        package_manager.save()
        exit(0)
    except Exception as e:
        raise e
        print('Operation failed with Error: ', e)
        exit(1)
