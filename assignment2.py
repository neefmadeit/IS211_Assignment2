import argparse
import sys
import logging
from datetime import datetime, date
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import io
import csv

LOG_NAME = 'assignment2'
LOG_FILENAME = 'error.log'

"""Download contents from the given URL and return it as decoded text."""

def downloadData(url: str) -> str:

    with urlopen(url) as resp:
        charset = resp.headers.get_content_charset() or 'utf-8'
        data = resp.read()
        try:
            return data.decode(charset)
        except UnicodeDecodeError:
            return data.decode('latin-1')

"""Process the CSV file"""

def processData(file_content: str) -> dict:

    logger = logging.getLogger(LOG_NAME)
    personData = {}

    reader = csv.reader(io.StringIO(file_content))
    for line_num, row in enumerate(reader, start=1):
        if not row:
            continue
        if len(row) < 3:
            continue

        raw_id = row[0].strip()
        name = row[1].strip()
        bday_str = row[2].strip()

        try:
            pid = int(raw_id)
        except ValueError:
            continue

        try:
            bday_dt = datetime.strptime(bday_str, "%d/%m/%Y").date()
        except ValueError:
            logger.error(f"Error processing line #{line_num} for ID #{pid}")
            continue

        personData[pid] = (name, bday_dt)

    return personData

""" Prints person info or 'No user found with that id'. """

def displayPerson(pid: int, personData: dict) -> None:

    if pid not in personData:
        print("No user found with that id")
        return
    name, bday = personData[pid]
    print(f"Person #{pid} is {name} with a birthday of {bday.strftime('%Y%m%d')}")

"""Configure logger 'assignment2' to write ERROR messages to a single file."""

def _configure_logging() -> None:

    logger = logging.getLogger(LOG_NAME)
    logger.setLevel(logging.ERROR)

    if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
        fh = logging.FileHandler(LOG_FILENAME, mode='w', encoding='utf-8')
        fh.setLevel(logging.ERROR)
        fh.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(fh)

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download, process, and query person data from a CSV URL."
    )
    # URL is required (no default)
    parser.add_argument('url', help='URL pointing to the CSV file')
    args = parser.parse_args()

    # Download (catch and report any errors)
    try:
        csvData = downloadData(args.url)
    except (HTTPError, URLError, ValueError, OSError) as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)

    # Configure logging and process
    _configure_logging()
    personData = processData(csvData)

    # Interactive loop
    while True:
        try:
            user_in = input("Please enter an ID to lookup: ").strip()
            pid = int(user_in)
        except ValueError:
            print("Please enter a valid integer ID.")
            continue

        if pid <= 0:
            break

        displayPerson(pid, personData)

if __name__ == '__main__':
    main()