import os
import sys
import time
import requests

from . import __version__
from .sponsors import SPONSORS

TEAL = "\033[38;5;50m"
GREY = "\033[38;5;245m"
BOLD = "\033[1m"
RESET = "\033[0m"
#######################
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BLACK = "\033[90m"
RESET = "\033[0m"
#######################
BF1 = "\033[38;5;51m"
BF2 = "\033[38;5;50m"
BF3 = "\033[38;5;49m"
BF4 = "\033[38;5;48m"
BF5 = "\033[38;5;44m"
BF6 = "\033[38;5;43m"
BF7 = "\033[38;5;38m"
BF8 = "\033[38;5;37m"
BF9 = "\033[38;5;32m"
#######################

LOGO = r"""
 ███╗   ███╗ █████╗  ██████╗ ███╗   ██╗███████╗███████╗██╗██╗   ██╗███╗   ███╗ 
 ████╗ ████║██╔══██╗██╔════╝ ████╗  ██║██╔════╝██╔════╝██║██║   ██║████╗ ████║ 
 ██╔████╔██║███████║██║  ███╗██╔██╗ ██║█████╗  ███████╗██║██║   ██║██╔████╔██║ 
 ██║╚██╔╝██║██╔══██║██║   ██║██║╚██╗██║██╔══╝  ╚════██║██║██║   ██║██║╚██╔╝██║ 
 ██║ ╚═╝ ██║██║  ██║╚██████╔╝██║ ╚████║███████╗███████║██║╚██████╔╝██║ ╚═╝ ██║ 
 ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝     ╚═╝ 
"""

def drawnews():
    rurl = "https://raw.githubusercontent.com/Drowys22/magnesium/main/news.json"
    rudata = requests.get(rurl).json()

    print(f"{BLACK}-----------------------------------------------------------------------------{RESET}") # 77ch -2 = 75ch : ( 75 - len(item) ) / 2
    for item in rudata["news"]:
        print(f"{BLACK}|{BF1}{item.center(75)}{BLACK}|{RESET}")
    print(f"{BLACK}-----------------------------------------------------------------------------{RESET}")
    print(" ")
def enable_ansi() -> None:
    """Windows 10+"""
    if os.name == "nt":
        os.system("")


def _sleep(seconds: float, fast: bool) -> None:
    if not fast:
        time.sleep(seconds)


def _progress_bar(label: str, fast: bool, width: int = 30) -> None:
    steps = [width] if fast else range(width + 1)
    for i in steps:
        bar = "█" * i + "░" * (width - i)
        sys.stdout.write(f"\r{GREY}{label:<18}{TEAL}{bar}{GREY} {int(i / width * 100):>3}%{RESET}")
        sys.stdout.flush()
        _sleep(0.015, fast)
    sys.stdout.write("\n")



def play(fast: bool = False) -> None:
    logograd = [51, 50, 44, 38, 32, 26]
    os.system("cls" if os.name == "nt" else "clear")
    print("")
    drawnews()
    enable_ansi()
 
    lines = [l for l in LOGO.splitlines() if l.strip()]
    for i, line in enumerate(lines):
        color = f"\033[38;5;{logograd[min(i, len(logograd) - 1)]}m"
        print(f"{color}{BOLD}{line}{RESET}")
        _sleep(0.08, fast)

    print(f" {GREY}v{__version__}{RESET}\n")

    _progress_bar("  loading modules...", fast)
    _progress_bar("  commands...", fast)

    if SPONSORS:
        print(f"\n{GREY}  Founding sponsors:{RESET}")
        for s in SPONSORS:
            url = f" {GREY}({s['url']}){RESET}" if s.get("url") else ""
            print(f"  {TEAL}{BOLD}{s['name']}{RESET}{url}")
            _sleep(0.15, fast)

    print()
