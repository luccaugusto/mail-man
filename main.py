#!/bin/python3
import sys
from options import options
from package_manager import PackageManager, Package
from track_bot import TrackBot
from commands import Commands
from ui_display import UIDisplay, ASCIIArt  # Import the new UI system


def track_all(package_manager: PackageManager) -> None:
    print(ASCIIArt.tracking_all_header())

    # Show packages being tracked with new formatting
    pending_packages = [p for p in package_manager.package_list if p.delivered == "False"]
    if pending_packages:
        for package in pending_packages:
            print(UIDisplay.format_package_entry(package))
    print("")

    if options.show_delivered:
        print(ASCIIArt.package_delivered())
        delivered_packages = [p for p in package_manager.package_list if p.delivered == "True"]
        if delivered_packages:
            for package in delivered_packages:
                print(UIDisplay.format_package_entry(package, show_delivered_status=True))

    track_bot = TrackBot()
    statuses = track_bot.track(package_manager.package_list)

    package_manager.assign_statuses(statuses)
    package_manager.show_package_statuses()
    package_manager.mark_delivered(statuses)
    if not options.keep_delivered:
        package_manager.remove_delivered(statuses)


def track_single(code: str) -> None:
    print(ASCIIArt.single_package_box(code, "Tracking single package"))
    track_bot = TrackBot()
    package = Package(code)
    status = track_bot.track_single(package.code)
    package_status = next(s for s in status["transito"] if s["cod_objeto_"] == package.code)
    if package_status is None:
        package_status = next(s for s in status["entregue"] if s["cod_objeto_"] == package.code)

    package.set_status(package_status)
    package_manager.show_single_package_status(package)


if __name__ == "__main__":
    UIDisplay.show_startup_banner()

    args = sys.argv[1:]

    options.parse_opts(args)

    try:
        package_manager = PackageManager()

        if options.command == Commands.ADD.value:
            package_manager.add_package(options.code, label=options.label)

        elif options.command == Commands.HELP.value:
            Commands.show_help()

        elif options.command == Commands.TRACK_SINGLE.value:
            track_single(options.code)

        elif options.command == Commands.REMOVE.value:
            package_manager.remove_package(options.code)

        elif options.command == Commands.LIST.value:
            package_manager.show_packages()

        elif options.command == Commands.LIST_ALL.value:
            package_manager.show_packages(show_delivered=True)

        elif options.command == Commands.TRACK_ALL.value:
            track_all(package_manager)

        elif options.command == Commands.REMOVE_ALL.value:
            package_manager.drop_package_list()

        elif options.command == Commands.HELP_LONG.value:
            Commands.show_help()
        elif options.command == Commands.FETCH_CAPTCHAS.value:
            track_bot = TrackBot()
            track_bot.fetch_a_bunch_of_captchas(options.number_of_captchas_to_fetch)
        else:
            Commands.show_help()

        package_manager.save()
        exit(0)
    except Exception as e:
        print(ASCIIArt.error_message(str(e)))
        exit(1)
