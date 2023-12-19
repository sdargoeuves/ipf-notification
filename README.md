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

You can run the script with the following command:

```shell
python check_discovery.py
#You can also specify a warning threshold in minutes:
python check_discovery.py --threshold 120
```

## Configuration

The script uses the following environment variables:

- `WARNING_THRESHOLD`: The warning threshold in minutes. If a discovery job has been running for longer than this threshold, a warning will be logged. Default is 60 minutes.

## License

This project is licensed under the MIT License.
