import os

import typer
from dotenv import find_dotenv, load_dotenv
from ipfabric import IPFClient

from modules.models import DiscoveryJobChecker

# Load environment variables
load_dotenv(find_dotenv(usecwd=True), override=True)

app = typer.Typer(add_completion=False)

@app.command()
def main(
    warning_threshold: int = typer.Option(
        None,
        "-t",
        "--threshold",
        help="Warning threshold in minutes",
    )
) -> None:
    """
    Checks if there is a running discovery job, and check the running time
    """
    if os.getenv("IPF_URL") is not None and os.getenv("IPF_TOKEN") is not None:
        ipf = IPFClient(base_url=os.getenv("IPF_URL"), auth=os.getenv("IPF_TOKEN"), verify=False, timeout=20)
        discovery_checker = DiscoveryJobChecker(ipf, warning_threshold)
        discovery_checker.check_discovery_jobs()

    if os.getenv("IPF_URL_2") is not None and os.getenv("IPF_TOKEN_2") is not None:
        ipf = IPFClient(base_url=os.getenv("IPF_URL_2"), auth=os.getenv("IPF_TOKEN_2"), verify=False, timeout=20)
        discovery_checker = DiscoveryJobChecker(ipf, warning_threshold)
        discovery_checker.check_discovery_jobs()

if __name__ == "__main__":
    app()
