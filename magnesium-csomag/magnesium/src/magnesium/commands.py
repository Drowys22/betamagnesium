import os
import platform
import sys
from typing import Callable, Dict, Tuple
from . import __version__
import socket
import requests
from ping3 import ping
import time
import speedtest

REGISTRY: Dict[str, Tuple[Callable[[list], None], str]] = {}
slink = "soon"

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

def command(name: str, help_text: str):
    def decorator(func):
        REGISTRY[name] = (func, help_text)
        return func

    return decorator


@command("help", "List of available commands")
def cmd_help(args):
    print(" ")
    print(f"{WHITE}[{GRAY}Magnesium{WHITE}] Available commands:{RESET}")
    print(" ")
    for name in sorted(REGISTRY):
        i = list(sorted(REGISTRY)).index(name) + 1
        i = str(i).zfill(2)
        print(f"    {WHITE}[{i}] [{BF1}c{BF4}m{BF9}d{WHITE}]  {WHITE}{name:<10} {GRAY} | {REGISTRY[name][1]}{RESET}")
    print(" ")


@command("speedtest", "Test your internet speed")
def cmd_speedtest(args):

    def lbar():
        phases = [
            "Initializing Network Stack",
            "Finding Best Server",
            "Connecting to Server",
            "Preparing Speed Test",
            "Starting Measurement"
        ]

        for i in range(15):
            os.system("cls" if os.name == "nt" else "clear")
            frame = ["\\", "-", "|", "/", "\\", "-", "|", "/", "\\", "-", "|", "/", "\\", "-", "|"][i]

            print("\n\n")
            print(
                f"  {frame}  {MAGENTA}["
                f"{CYAN}{'█' * (i + 1)}"
                f"{'░' * (14 - i)}"
                f"{MAGENTA}]{RESET}"
            )
            phase = min(i // 3, 4)
            print(
                f"\n      {WHITE}{phases[phase]}{RESET}")
            time.sleep(0.15)
    try:
        print(f"\n{BLACK}[Speedtest] {BF1}Initializing {BF9}Speedtest...{RESET}")

        lbar()

        st = speedtest.Speedtest()

        print(f"\n{BLACK}[Speedtest] {BF2}Finding {BF9}best{BF2} server...{BLACK} (could take a moment){RESET}")
        server = st.get_best_server()

        print(
            f"            {GREEN}Connected to: "
            f"{server['sponsor']}{RESET}"
        )

        print(f"\n{BLACK}[Speedtest] {BF3}Testing {BF9}download...{RESET}")
        download = st.download() / 1_000_000

        print(f"{BLACK}[Speedtest] {BF4}Testing {BF9}upload...{RESET}")
        upload = st.upload() / 1_000_000

        ping_time = st.results.ping

        print(f"\n{BLACK}[Speedtest] {BF5}Results:{RESET}")

        print(f"{BF6}                {BLACK}[1]{RESET} Download: {download:.2f} Mbps{RESET}")
        print(f"{BF7}                {BLACK}[2]{RESET} Upload:       {upload:.2f} Mbps{RESET}")
        print(f"{BF8}                {BLACK}[3]{RESET} Ping:     {ping_time:.2f} ms{RESET}")

        print(f"\n{BLACK}[Speedtest] {RED}If you have a great time, please support us on {BF9}{slink} ❤️{RESET}")

    except speedtest.ConfigRetrievalError:
        print(f"{RED}Could not retrieve speedtest configuration.{RESET}")

    except speedtest.SpeedtestException as e:
        print(f"{RED}Speedtest error: {e}{RESET}")

    except Exception as e:
        print(f"{RED}Unexpected error: {e}{RESET}")


@command("myip", "Show local and public IP addresses")
def cmd_myip(args):
    lip = socket.gethostbyname(socket.gethostname())  # localip
    try:
        puip = requests.get("https://api.ipify.org").text # publicip
    except requests.RequestException:
        puip = f"{RED} Error! Could not retrieve public IP{RESET}"

    print(f"\n{RESET}[{YELLOW}MyIP{RESET}] Local IP:  {lip}")
    print(f"[{YELLOW}MyIP{RESET}] Public IP: {puip}\n")

@command("pwd", "Print the current working directory")
def cmd_pwd(args):
    try:
        print("")
        print(f"{GRAY}  ----------------------{RESET}" + (int(os.get_terminal_size().columns - 26) - 2) * f"{GRAY}-{RESET}")
        print(f"{GRAY}  | Directory{WHITE} -→ {BF1}{os.getcwd()}{RESET}" + (int(os.get_terminal_size().columns - 22) - len(os.getcwd())) * f"{GRAY} {GRAY}" + "|")
        print(f"{GRAY}  ----------------------{RESET}" + (int(os.get_terminal_size().columns - 26) - 2) * f"{GRAY}-{RESET}")
        print("")
    except FileNotFoundError:
        print(f"{RED}Error: The current directory no longer exists.{RESET}")

@command("ls", "List files and directories in current path")
def cmd_ls(args):
    try:
        items = os.listdir(os.getcwd())
        if not items:
            print(f"{RED}Directory is empty.{RESET}")
            return
        
        for item in sorted(items):
            full_path = os.path.join(os.getcwd(), item)
            if os.path.isdir(full_path):
                print(f"  {BLUE}[DIR] {item}{RESET}")
            else:
                print(f"  {WHITE}      {item}{RESET}")
    except Exception as e:
        print(f"{RED}Error reading directory: {e}{RESET}")

@command("dns", "Resolve fast a domain name")
def cmd_dns(args):
    if not args:
        print(f"\n{RED}Usage: dns <domain>{RESET}\n")
        return
    dnshost = args[0]

    try:
        results = socket.getaddrinfo(dnshost, None)
        addresses = sorted({
            result[4][0] for result in results
        })
        print(f"\n{CYAN}DNS Lookup: {dnshost}{RESET}\n")
        for address in addresses:
            print(f"\n{GREEN}→ {address}{RESET}\n")
    except socket.gaierror:
        print(f"\n{RED}DNS lookup failed.{RESET}\n")

@command("cat", "Print file contents") # 2.1
def cmd_cat(args):
    if not args:
        print(f"\n{RED}[INVALID] Usage: cat <file>{RESET}\n")
        return
    
    catpath = " ".join(args)
    try:
        with open(catpath, "r", encoding="utf-8") as file:
            for a in file:
                print(a, end="")
    except FileNotFoundError:
        print(f"\n{RED}[INVALID] File not found: {catpath}{RESET}\n")
    except UnicodeDecodeError:
        print(f"\n{RED}[INVALID] Cannot decode this file as UTF-8.{RESET}\n")
    except PermissionError:
        print(f"\n{RED}[INVALID] Permission denied.{RESET}\n")

@command("cd", "Change the current working directory")
def cmd_cd(args):
    if not args:
        print(f"\n{BLUE}User {RED}Error: No path provided.{RESET}\nUsage: cd <path>\n") # visszadob
        return
    
    tarp = " ".join(args)
    try:
        os.chdir(tarp)
    except FileNotFoundError:
        print(f"{RED}Error: The directory '{tarp}' does not exist.{RESET}")
    except NotADirectoryError:
        print(f"{RED}Error: '{tarp}' is not a directory.{RESET}")
    except PermissionError:
        print(f"{RED}Error: Permission denied for '{tarp}'.{RESET}")
    except Exception as e:
        print(f"{RED}Error changing directory: {e}{RESET}")


@command("version", "Show the installed version")
def cmd_version(args):
    print(f"Magnesium {__version__}")


@command("sysinfo", "System default datas")
def cmd_sysinfo(args):
    print(f"OS:      {platform.system()} {platform.release()}")
    print(f"Python:  {sys.version.split()[0]}")
    print(f"Directory:   {os.getcwd()}")


@command("clear", "Clear the CLI")
def cmd_clear(args):
    os.system("cls" if os.name == "nt" else "clear")


@command("exit", "Exit")
def cmd_exit(args):
    raise SystemExit(0)

@command("ping", "Ping a Website")
def cmd_ping(args):

    def lbar():
        statusbar = 0
        for i in range(15):
            statusbar += 1
            os.system("cls" if os.name == "nt" else "clear")
            print()
            print()
            if statusbar in (1, 9):
                print(
                     f"  \  {MAGENTA}[{CYAN}{'█' * (i + 1)}{'░' * (15 - (i + 1))}{MAGENTA}]{RESET}"
                )
            elif statusbar in (2, 10):
                print(
                     f"  -  {MAGENTA}[{CYAN}{'█' * (i + 1)}{'░' * (15 - (i + 1))}{MAGENTA}]{RESET}"
                )
            elif statusbar in (3, 11):
                print(
                     f"  |  {MAGENTA}[{CYAN}{'█' * (i + 1)}{'░' * (15 - (i + 1))}{MAGENTA}]{RESET}"
                )
            elif statusbar in (4, 12):
                print(
                     f"  \  {MAGENTA}[{CYAN}{'█' * (i + 1)}{'░' * (15 - (i + 1))}{MAGENTA}]{RESET}"
                )
            elif statusbar in (5, 13):
                print(
                     f"  -  {MAGENTA}[{CYAN}{'█' * (i + 1)}{'░' * (15 - (i + 1))}{MAGENTA}]{RESET}"
                )
            elif statusbar in (6, 14):
                print(
                     f"  /  {MAGENTA}[{CYAN}{'█' * (i + 1)}{'░' * (15 - (i + 1))}{MAGENTA}]{RESET}"
                )
            elif statusbar in (7, 15):
                print(
                     f"  |  {MAGENTA}[{CYAN}{'█' * (i + 1)}{'░' * (15 - (i + 1))}{MAGENTA}]{RESET}"
                )
            elif statusbar == 8:
                print(
                     f"    {MAGENTA}[{CYAN}{'█' * (i + 1)}{'░' * (15 - (i + 1))}{MAGENTA}]{RESET}"
                )
            if i < 3:
                currentlyworkingon = "Initializing Network Stack"
            elif i < 6:
                        currentlyworkingon = f"Resolving {args}"
            elif i < 9:
                        currentlyworkingon = "Connecting to Host"
            elif i < 12:
                        currentlyworkingon = "Performing ICMP Handshake"
            elif i < 15:
                        currentlyworkingon = "Measuring Latency"
            else:
                currentlyworkingon = "   Finished"
            print(
                f"      {WHITE}{currentlyworkingon}{RESET}"
            )
            print()
            time.sleep(0.5)
        statusbar = 0
    
    
    if not args:
        lbar()
        print(f"\n{BLUE}User {RED}Error: No host provided{BLUE}\nUsage: {RED}ping <host>{RESET}\n")
        return
    
    def resolvehost(host):
        try:
            return socket.gethostbyname(host)
        except:
            return "Unknown IP"
    
    progress = 0
    average = 0
    for i in range(15):
        progress += 1
        os.system("cls" if os.name == "nt" else "clear")
        print()
        print()
        print(
             f"     {MAGENTA}[{CYAN}{'█' * progress}{'░' * (15 - progress)}{MAGENTA}]{RESET}"
        )
        if progress < 3:
            currentlyworkingon = "Initializing Network Stack"
        elif progress < 6:
                    currentlyworkingon = f"Resolving {args}"
                    host = args[0]
                    hostip = resolvehost(host)
        elif progress < 9:
                    currentlyworkingon = f"Connecting to {hostip}"
        elif progress < 12:
                    currentlyworkingon = "Performing ICMP Handshake"
        elif progress < 15:
                    currentlyworkingon = "Measuring Latency"
        else:
            currentlyworkingon = "   Finished"
        print(
            f"      {WHITE}{currentlyworkingon}{RESET}"
        )
        print()

    if hostip == "Unknown IP":
        print(f"\n{BLUE}User {RED}Error: {BLUE}{host}{RED} is unreachable{BLUE}\nUsage: {RED}ping <host>{RESET}\n")
        return

    result = ping(host, unit="ms")
    for i in range(15):
        if result is None or result == 0:
              print(
                   f"      {MAGENTA}[{RESET}{i+1}{MAGENTA}]{BLACK}-{MAGENTA}[{RESET}{host}{MAGENTA}] {RED}Host unreachable{BLACK} / {RED}ERROR{RESET}"
              ) 
        else:
              ping_time = round(result, 1)
              print(
                   f"      {MAGENTA}[{RESET}{i+1}{MAGENTA}]{BLACK}-{MAGENTA}[{RESET}{host}{MAGENTA}] Ping: {RESET}{ping_time} ms"
              )
        average += ping_time
        time.sleep(1)
    print("")
    print(f"{BLACK}Average ping time: {MAGENTA}{average / 15}{RESET}")


def run(line: str) -> None:
    parts = line.strip().split()
    if not parts:
        return
    name, args = parts[0].lower(), parts[1:]
    if name not in REGISTRY:
        print(f"Unknown command: {name}  (try: help)")
        return
    REGISTRY[name][0](args)
