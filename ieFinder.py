#!/usr/bin/python3
import logging
import argparse
import os
import sys
from datetime import datetime

import certstream
from art import text2art
from termcolor import cprint
from colorama import init, Fore, Style

init(autoreset=True)

# Initialize logging
logging.basicConfig(filename="logs/certstream.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Argument parser setup
parser = argparse.ArgumentParser(
    description="Finds and logs .ie domain names by checking certificate transparency logs in near realtime."
)
parser.add_argument(
    "-v",
    "--verbose",
    help="verbose output (All tlds passing through, not just the .ie tld).",
    required=False,
    action="store_true",
)
args = vars(parser.parse_args())


def on_certstream_error(exception):
    logging.error("Exception in CertStreamClient! -> %s", exception)


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def write_to_log_files(domain, clean, www):
    """
    Writes domain information to various log files.

    Args:
        domain (str): The full domain name including subdomains.
        clean (str): The domain name.
        www (str): The domain name with 'www'.
    """
    timestamp = get_timestamp()

    if not os.path.exists("logs"):
        os.makedirs("logs")

    with open(os.path.join("logs", "log.txt"), "a", encoding="utf-8") as f:
        f.write(domain + "\n")
    with open(os.path.join("logs", "domains.txt"), "a", encoding="utf-8") as f:
        f.write(clean + "\n")
    with open(os.path.join("logs", "domains.csv"), "a", encoding="utf-8") as f:
        f.write(f"{timestamp},{clean}\n")
    with open(os.path.join("logs", "www.txt"), "a", encoding="utf-8") as f:
        f.write(f"{www}\n")


def print_callback(message, context):
    """
    Callback function to handle messages from CertStream.

    Args:
        message (dict): The message received from CertStream.
        context (dict): The context of the message.
    """
    timestamp = get_timestamp()

    if message["message_type"] == "heartbeat":
        return
    if message["message_type"] == "certificate_update":
        all_domains = message["data"]["leaf_cert"]["all_domains"]

        if len(all_domains) == 0:
            domain = "NULL"
        else:
            domain = all_domains[0]

            if args["verbose"]:
                print(f"{Style.DIM}[{timestamp}]: {domain}")

            if domain.endswith(".ie"):
                clean_domain_name = domain.split(".")[-2] + "." + domain.split(".")[-1]
                www_domain_name = "www." + domain.split(".")[-2] + "." + domain.split(".")[-1]
                write_to_log_files(domain, clean_domain_name, www_domain_name)
                url = f"https://{domain}"
                print(f"{Style.DIM}[{timestamp}]{Style.RESET_ALL}{Fore.GREEN} {hyperlink(url, domain)}")

        sys.stdout.flush()


def hyperlink(uri, label=None):
    if label is None:
        label = uri

    parameters = ""
    escape_mask = "\033]8;{};{}\033\\{}\033]8;;\033\\"
    return escape_mask.format(parameters, uri, label)


def main():
    cprint(text2art(".ie   Finder"), "green", end=" ")
    print(
        f'{Fore.GREEN}The .ie do{Fore.WHITE}main na{Fore.LIGHTYELLOW_EX}me finder{Fore.RESET}{Style.DIM} | {hyperlink("https://github.com/senf666/iefinder", "Github")}\n'
    )

    certstream.listen_for_events(print_callback, on_error=on_certstream_error, url="wss://certstream.calidog.io/")


# -------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
