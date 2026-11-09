import argparse
import sys
import os

from . import __version__, animation, commands

####################### colors
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BLACK = "\033[90m"
GRAY = "\033[38;5;245m"
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
fadecolors = [BF1, BF2, BF3, BF4, BF5, BF6, BF7, BF8, BF9]
#######################

def spath(depth: int = 1) -> str:
    try:
        cwd = os.getcwd()
    except FileNotFoundError:
        return "?"
    if cwd == os.path.expanduser("~"):
        return "~"
    parts = cwd.replace("\\", "/").rstrip("/").split("/")
    if len(parts) <= depth:
        return cwd
    return ".../" + "/".join(parts[-depth:])


def build_prompt() -> str:
    name = f"{BF1}M{BF2}a{BF3}g{BF4}n{BF5}e{BF6}s{BF7}i{BF8}u{BF9}m"
    return f" {GRAY}{spath()} {name}{BLACK} > {RESET}"

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="magnesium", description="Magnesium – For a better experience.")
    parser.add_argument("--no-anim", action="store_true", help="Skip startup animation")
    parser.add_argument("--version", action="version", version=f"Magnesium {__version__}")
    parser.add_argument("command", nargs="*", help="Run a single command in non-interactive mode")
    args = parser.parse_args(argv)

    fast = args.no_anim or not sys.stdout.isatty()

    if args.command:
        commands.run(" ".join(args.command))
        return 0

    animation.play(fast=fast)
    print("  Type: help\n") ## au. printes
    try:
        while True:
            try:
                line = input(build_prompt())
            except EOFError:
                break
            commands.run(line)
    except (KeyboardInterrupt, SystemExit):
        pass
    return 0
