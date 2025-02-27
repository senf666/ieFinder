#!/usr/bin/python3
import logging
import sys
import certstream
import argparse
import time
from art import *
from termcolor import cprint, colored
import sys
import datetime
from colorama import init, Fore, Back, Style
import sys
import os


logging.basicConfig(
    filename="logs/certstream.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)
init(autoreset=True)

parser = argparse.ArgumentParser(
    description="Finds and logs .ie domain names by checking certfiicate transparency logs in near realtime."
)
parser.add_argument(
    "-v",
    "--verbose",
    help="verbose output (All domains passing through).",
    required=False,
    action="store_true",
)
args = vars(parser.parse_args())

# -------------------------------------------------------------------------------


def on_error(exception):
    logging.error(f"Exception in CertStreamClient! -> {exception}")


# -------------------------------------------------------------------------------


def write_to_files(domain, clean, www):
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

    if not os.path.exists("logs"):
        os.makedirs("logs")

    with open(os.path.join("logs", "log.txt"), "a") as f:
        f.write(domain + "\n")
    with open(os.path.join("logs", "domains.txt"), "a") as f:
        f.write(clean + "\n")
    with open(os.path.join("logs", "domains.csv"), "a") as f:
        f.write(f"{timestamp},{clean}\n")
    with open(os.path.join("logs", "www.txt"), "a") as f:
        f.write(f"{www}\n")


# -------------------------------------------------------------------------------


def print_callback(message, context):
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

    if message["message_type"] == "heartbeat":
        return
    if message["message_type"] == "certificate_update":
        all_domains = message["data"]["leaf_cert"]["all_domains"]

        if len(all_domains) == 0:
            domain = "NULL"
        else:
            domain = all_domains[0]

            if args["verbose"] is True:
                print(f"{Style.DIM}[{timestamp}]: {domain}")

            if domain.endswith(".ie"):
                clean_domain_name = (
                    domain.split(".")[len(domain.split(".")) - 2]
                    + "."
                    + domain.split(".")[len(domain.split(".")) - 1]
                )
                www_domain_name = (
                    "www."
                    + domain.split(".")[len(domain.split(".")) - 2]
                    + "."
                    + domain.split(".")[len(domain.split(".")) - 1]
                )
                write_to_files(domain, clean_domain_name, www_domain_name)
                url = f"https://{domain}"
                print(
                    f"{Style.DIM}[{timestamp}]{Style.RESET_ALL}{Fore.GREEN} {hyperlink(url,domain)}"
                )

        sys.stdout.flush()


# -------------------------------------------------------------------------------


def hyperlink(uri, label=None):
    if label is None:
        label = uri

    parameters = ""
    escape_mask = "\033]8;{};{}\033\\{}\033]8;;\033\\"
    return escape_mask.format(parameters, uri, label)


# -------------------------------------------------------------------------------


def main():
    cprint(text2art(".ie   Finder"), "green", end=" ")
    print(
        f'{Fore.GREEN}The .ie do{Fore.WHITE}main na{Fore.LIGHTYELLOW_EX}me finder{Fore.RESET}{Style.DIM} | {hyperlink("https://github.com/senf666/iefinder","Github")}\n'
    )

    certstream.listen_for_events(print_callback, url="wss://certstream.calidog.io/")


# -------------------------------------------------------------------------------


if __name__ == "__main__":
    main()
