import logging
import os

import typer
from dotenv import find_dotenv, load_dotenv
from ipfabric import IPFClient

from modules.models import DiscoveryJobChecker

# Constants
SEND_EMAIL = False
DEFAULT_WARNING_THRESHOLD = 60  # in minutes

# Load environment variables
load_dotenv(find_dotenv(usecwd=True), override=True)

app = typer.Typer(add_completion=False)

@app.command()
def main(
    warning_threshold: int = typer.Option(
        os.getenv("WARNING_THRESHOLD", DEFAULT_WARNING_THRESHOLD),
        "-t",
        "--threshold",
        help="Warning threshold in minutes",
    )
) -> None:
    """
    Checks if there is a running discovery job, and check the running time
    """
    ipf = IPFClient(verify=False, timeout=20)
    discovery_checker = DiscoveryJobChecker(ipf, warning_threshold, send_mail_bool=SEND_EMAIL)
    discovery_checker.check_discovery_jobs()

if __name__ == "__main__":
    app()
