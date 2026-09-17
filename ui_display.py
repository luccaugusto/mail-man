#!/usr/bin/env python3
"""
UI Display Module for Mail-man
Contains ASCII art, colors, and display utilities to make the program look cool
"""

# Color codes for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'  # End color formatting


_MAILMAN = r"""
         ,
    _.-"` `'-.
   '._ __{}_(
     |'--.__\
    (   ^_\^
     |   _ |
     )\___/
 .--'`:._]
/  \      '-.
"""

_TITLE = [
    f"{Colors.CYAN}{Colors.BOLD}╔╦╗╔═╗╦╦    ╔╦╗╔═╗╔╗╔{Colors.END}",
    f"{Colors.CYAN}{Colors.BOLD}║║║╠═╣║║    ║║║╠═╣║║║{Colors.END}",
    f"{Colors.CYAN}{Colors.BOLD}╩ ╩╩ ╩╩╩═╝  ╩ ╩╩ ╩╝╚╝{Colors.END}",
    "",
    f"{Colors.YELLOW}don't lose your shit yo{Colors.END}",
]

class ASCIIArt:
    """Collection of ASCII art for the mail-man program"""
    
    @staticmethod
    def mail_man_banner():
        """Mailman art with the program name beside it, vertically centered"""
        art = _MAILMAN.strip("\n").splitlines()
        offset = (len(art) - len(_TITLE)) // 2
        column = max(len(line) for line in art) + 4
        rows = []
        for i, art_line in enumerate(art):
            title = _TITLE[i - offset] if offset <= i < offset + len(_TITLE) else ""
            gap = " " * (column - len(art_line))
            rows.append(f"{Colors.CYAN}{art_line}{Colors.END}{gap}{title}".rstrip())
        return "\n" + "\n".join(rows) + "\n"

    @staticmethod
    def package_in_transit():
        return f"""{Colors.YELLOW}{Colors.BOLD}📦 PACKAGES IN TRANSIT 📦{Colors.END} """

    @staticmethod
    def package_delivered():
        return f"""{Colors.GREEN}🏠 {Colors.BOLD} DELIVERED PACKAGES 📦{Colors.END} """

    @staticmethod
    def tracking_all_header():
        """Header for tracking all packages"""
        return f"""{Colors.BLUE}{Colors.BOLD}🔍 TRACKING ALL PACKAGES 🔍{Colors.END} """

    @staticmethod
    def captcha_solving():
        """ASCII art for captcha solving"""
        return f""" 
{Colors.MAGENTA}🔓 {Colors.BOLD}SOLVING CAPTCHA{Colors.END}{Colors.MAGENTA} 🔓{Colors.END} """

    @staticmethod
    def single_package_box(code, label=""):
        """Create a nice box for a single package"""
        display_text = f"{code} - {label}" if label else code
        padding = max(0, 50 - len(display_text))
        left_pad = padding // 2
        right_pad = padding - left_pad
        
        return f""" {Colors.CYAN}    📦 {Colors.BOLD}{display_text}{Colors.END} {Colors.CYAN}📦{Colors.END} """

    @staticmethod
    def delivery_status_icon(status):
        """Get appropriate emoji/icon for delivery status"""
        if status == "entregue":
            return f"{Colors.GREEN}✅ DELIVERED{Colors.END}"
        elif status == "transito":
            return f"{Colors.YELLOW}🚚 IN TRANSIT{Colors.END}"
        else:
            return f"{Colors.RED}❓ UNKNOWN{Colors.END}"

    @staticmethod
    def package_list_header():
        """Header for package listing"""
        return f""" {Colors.BLUE}    📋 PACKAGE LIST 📋{Colors.END} """

    @staticmethod
    def error_message(message):
        """Format error messages with ASCII art"""
        return f""" {Colors.RED}{Colors.BOLD}    ⚠️  ERROR: {message} ⚠️{Colors.END} """

    @staticmethod
    def success_message(message):
        """Format success messages with ASCII art"""
        return f""" {Colors.GREEN}{Colors.BOLD}    ✅ SUCCESS: {message} ✅{Colors.END} """

    @staticmethod
    def separator_line():
        """Create a decorative separator line"""
        return f"{Colors.CYAN}    {'═' * 75}{Colors.END}"


class UIDisplay:
    """Main UI display class with helper methods"""
    
    @staticmethod
    def show_startup_banner():
        """Display the startup banner"""
        print(ASCIIArt.mail_man_banner())
    
    @staticmethod
    def format_package_entry(package, show_delivered_status=False):
        """Format a single package entry with nice styling"""
        delivered_marker = ""
        if show_delivered_status and hasattr(package, 'delivered') and package.delivered == 'True':
            delivered_marker = f" {Colors.GREEN}[DELIVERED]{Colors.END}"
        
        return f"    {Colors.CYAN}📦{Colors.END} {Colors.BOLD}{package.code}{Colors.END} - {package.label}{delivered_marker}"
    
    @staticmethod
    def format_package_status_header(package):
        """Format package status header with cool styling"""
        return f"""{Colors.BLUE}    📦 {Colors.BOLD}{package.label} {package.code}{Colors.END}{Colors.BLUE} """
    
    @staticmethod
    def format_event_info(date, description, location, event_type=""):
        """Format event information with nice styling"""
        event_line = f"    {Colors.YELLOW}📅{Colors.END} {Colors.BOLD}{date}{Colors.END}"
        desc_line = f"    {Colors.CYAN}📍{Colors.END} {description}: {location}"
        if event_type:
            desc_line += f" {Colors.MAGENTA}{event_type}{Colors.END}"
        
        return f"{event_line}\n{desc_line}\n{ASCIIArt.separator_line()}"
    
    @staticmethod
    def format_prediction_info(prediction, package_type):
        """Format package prediction and type info"""
        return f"""    {Colors.GREEN}📅{Colors.END} Previsão: {Colors.BOLD}{prediction}{Colors.END}
    {Colors.BLUE}📋{Colors.END} Tipo: {Colors.BOLD}{package_type}{Colors.END}""" 