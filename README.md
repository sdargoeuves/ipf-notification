# Discovery Job - Email Notification

This project contains a script to check if there is a running discovery job and its running time.

## Requirements

- Python 3.8+
- Packages: typer, python-dotenv, ipfabric

## Installation

1. Clone the repository:

    ```shell
    git clone https://github.com/yourusername/discovery-job-checker.git
    ```

2. Install the required packages:

    ```shell
    pip install -r requirements.txt
    ```

3. Copy the `.env.sample` to `.env` and edit the variable according to your environment

```shell
cp .env.sample .env
vi .env
```

## Usage

To run the script, use the following command:

```shell
python check_discovery.py
# You can also specify a warning threshold in minutes:
python check_discovery.py --threshold 120
```

For continuous monitoring, it's recommended to run this script on a regular basis. One way to achieve this is by adding the script to a cron job. Here's an example of how to set up a cron job that runs the script every 4 hours:

Open the crontab file:

```shell
crontab -e
```

Add the following line to the file:

```shell
0 */4 * * * /usr/bin/python /path/to/check_discovery.py --threshold 240
```

Make sure to replace `/usr/bin/python` with the path to your Python interpreter, and `/path/to/check_discovery.py` with the path to the script.

Save and close the file. The new cron job will start running at the next scheduled time.

```note
Please note that the exact steps might vary depending on your operating system and environment.
```

## Configuration

The script uses the following environment variables:

- `WARNING_THRESHOLD`: The warning threshold in minutes. If a discovery job has been running for longer than this threshold, a warning will be logged. Default is 60 minutes.
- `SEND_EMAIL`: If set to `true`, an email will be sent when the warning threshold is exceeded. If set to `false`, the warning message will only be printed to the console.
- `EMAIL_FROM`: The email address that the warning emails will be sent from.
- `EMAIL_TO`: The email address that the warning emails will be sent to.
- `SMTP_SERVER`: The SMTP server that will be used to send the warning emails.
- `SMTP_PORT`: The port to use for the SMTP server.
- `SMTP_LOGIN`: The username to use for the SMTP server.
- `SMTP_PASSWORD`: The password to use for the SMTP server.
- `IPF_URL`: The URL of the IP Fabric instance to check.
- `IPF_TOKEN`: The API token to use for the IP Fabric instance.

You can also specify a second IP Fabric instance with the `IPF_URL_2` and `IPF_TOKEN_2` environment variables.

## License

This project is licensed under the MIT License.
