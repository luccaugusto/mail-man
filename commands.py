from enum import Enum
from ui_display import ASCIIArt, Colors  # Import the new UI system


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
        print(f"""
{Colors.BLUE}{Colors.BOLD}    ┌─────────────────────────────────────────────────────────────────────────┐
    │  📋 MAIL-MAN HELP & USAGE GUIDE 📋                                     │
    └─────────────────────────────────────────────────────────────────────────┘{Colors.END}

{Colors.YELLOW}{Colors.BOLD}    📦 USAGE:{Colors.END}
        {Colors.CYAN}mail-man [command] [tracking-code] [options]{Colors.END}

{Colors.YELLOW}{Colors.BOLD}    🎯 MAIN COMMANDS:{Colors.END}
        {Colors.GREEN}-a{Colors.END} {Colors.CYAN}[code]{Colors.END}          📥 Add a tracking code to the list
        {Colors.GREEN}-t{Colors.END} {Colors.CYAN}[code]{Colors.END}          🔍 Track a single package
        {Colors.GREEN}-r{Colors.END} {Colors.CYAN}[code]{Colors.END}          🗑️  Remove a package from the list
        {Colors.GREEN}-h{Colors.END} / {Colors.GREEN}--help{Colors.END}        ❓ Show this help text

{Colors.YELLOW}{Colors.BOLD}    📋 LIST COMMANDS:{Colors.END}
        {Colors.GREEN}--list{Colors.END}              📜 List packages being tracked
        {Colors.GREEN}--list-all{Colors.END}          📄 List tracked and delivered packages
        {Colors.GREEN}--track-all{Colors.END}         🚚 Track all packages from the list

{Colors.YELLOW}{Colors.BOLD}    🗑️  CLEANUP COMMANDS:{Colors.END}
        {Colors.GREEN}--remove-all{Colors.END}        🧹 Remove all packages from the list
        {Colors.GREEN}--keep{Colors.END}              💾 Keep delivered packages (default)
        {Colors.GREEN}--no-keep{Colors.END}           🗑️  Delete delivered packages automatically

{Colors.YELLOW}{Colors.BOLD}    🎨 DISPLAY OPTIONS:{Colors.END}
        {Colors.GREEN}--show-delivered{Colors.END}    📦 Show delivered packages when tracking
        {Colors.GREEN}--detailed{Colors.END}          📝 Show detailed event history

{Colors.MAGENTA}    ═══════════════════════════════════════════════════════════════════════════{Colors.END}
{Colors.CYAN}    💡 Example: {Colors.BOLD}mail-man -a AB123456789BR{Colors.END} {Colors.CYAN}to add a package{Colors.END}
{Colors.MAGENTA}    ═══════════════════════════════════════════════════════════════════════════{Colors.END}
""")
        exit(1)
