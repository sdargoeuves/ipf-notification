import logging
import os
import smtplib
import time
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from typing import Dict

from ipfabric import IPFClient

LOG_LEVEL = logging.INFO
WARNING_THRESHOLD = os.getenv("WARNING_THRESHOLD", 300)

# Setup logging
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

# from WARNING for httpx logs
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)

# from ERROR for ipfabric logs
ipfabric_logger = logging.getLogger("ipfabric")
ipfabric_logger.setLevel(logging.ERROR)

class DiscoveryJobChecker:
    """
    DiscoveryJobChecker class.
    A class that checks the status and duration of running discovery jobs.
    It provides methods to calculate the duration, format the duration and send email.

    Args:
        ipf (IPFClient): An instance of IPFClient used to interact with IP Fabric.
        warning_threshold (int): The threshold in minutes for the duration of a running discovery job.
    """
    def __init__(self, ipf: IPFClient, warning_threshold: int):
        self.ipf = ipf
        self.warning_threshold = WARNING_THRESHOLD if warning_threshold is None else warning_threshold
        self.send_email_bool = os.getenv('SEND_EMAIL', "false").lower() == "true"

    def check_discovery_jobs(self):
        running_discovery_job = self.ipf.jobs.all_jobs.all(
            filters={
                "status": ["eq", "running"],
                "name": ["eq", "discoveryNew"],
                "isDone": ["eq", "False"],
            }
        )

        if len(running_discovery_job) == 1:
            logger.info(f"{self.ipf.base_url.host} - One discovery running")
            self.check_discovery_time(running_discovery_job[0])
        elif len(running_discovery_job) == 0:
            logger.info(f"{self.ipf.base_url.host} - No discovery running")
        else:
            logger.error(f"{self.ipf.base_url.host} - UNEXPECTED - more than one running discovery job found")

    def check_discovery_time(self, running_discovery_job: Dict):
        duration = self.calculate_duration(running_discovery_job)
        running_discovery_job["duration_display"] = self.format_duration(duration)

        threshold_display = self.format_duration(self.warning_threshold * 60)
        running_discovery_job["threshold_display"] = threshold_display

        if duration > self.warning_threshold * 60:
            logger.warning(
                f"{self.ipf.base_url.host} - Threshold ({threshold_display}) exceeded - duration {running_discovery_job['duration_display']}"
            )
            logger.warning("Sending the notification email")
            self.send_email(running_discovery_job)
        else:
            logger.info(
                f"{self.ipf.base_url.host} - Threshold ({threshold_display}) not reached - duration {running_discovery_job['duration_display']} "
            )
            logger.info(f"{self.ipf.base_url.host} - No notification required")


    def send_email(self, running_discovery_job: Dict):
        email_from = os.getenv("EMAIL_FROM", "sender@example.com")
        email_to = os.getenv("EMAIL_TO", "recipient@example.com")
        smtp_server = os.getenv("SMTP_SERVER", None)
        smtp_port = os.getenv("SMTP_PORT", 25)
        smtp_login = os.getenv("SMTP_LOGIN", None)
        smtp_password = os.getenv("SMTP_PASSWORD", None)

        email = EmailMessage()
        email["From"] = email_from
        email["To"] = email_to
        email["Date"] = formatdate(localtime=True)  # Add the current date
        email["Message-Id"] = make_msgid()  # Generate a unique message ID
        email[
            "Subject"
        ] = f"IP Fabric - {self.ipf.base_url.host} - DISCOVERY WARNING - Threshold exceeded - {running_discovery_job['snapshot']}"
        email.set_content(
            f"""
    --- IP Fabric instance: {self.ipf.base_url.host} ---

    !!! Threshold Exceeded for Ongoing Discovery !!!
    Snapshot ID: {running_discovery_job['snapshot']}
    Started At: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(running_discovery_job['startedAt'] / 1000))} (UTC)
    Discovery Duration (hh:mm:ss): {running_discovery_job['duration_display']}
    Warning Threshold (hh:mm:ss): {running_discovery_job['threshold_display']}

    """
        )
        
        # for testing purposes, if email is not yet set, we can display in the logs
        if self.send_email_bool:
            with smtplib.SMTP(smtp_server, smtp_port) as smtp:
                smtp.login(smtp_login, smtp_password)
                smtp.send_message(email)
            logger.info(f"{self.ipf.base_url.host} - Email sent to {email_to}")
        else:
            logger.info(email)


    @staticmethod
    def calculate_duration(running_discovery_job: Dict) -> int:
        current_time = time.time()  # Time in seconds
        started_at = running_discovery_job["startedAt"] / 1000
        return current_time - started_at

    @staticmethod
    def format_duration(duration: int) -> str:
        duration_hours = format(int(duration // 3600), "02d")
        duration_minutes = format(int((duration % 3600) // 60), "02d")
        duration_seconds = format(int((duration % 3600) % 60), "02d")
        return f"{duration_hours}:{duration_minutes}:{duration_seconds}"
