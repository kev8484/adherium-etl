import csv
from io import FileIO
from datetime import datetime
import pysftp
from config import Config


config = Config()


def get_file(remote_dir, fname):
    # connect
    with pysftp.Connection(
        host=config.SFTP_HOSTNAME,
        username=config.SFTP_USERNAME,
        password=config.SFTP_PASSWORD,
    ) as sftp:
        logging.debug(f"Connection to {} successfully established.")
        # get file
        fo = FileIO()
        # fname = f"{datetime.today().strftime('%Y-%m-%d')}_DailyMedicationUsage.csv"
        sftp.getfo(f"{remote_dir}/{fname}", fo)
        logging.debug(f"Retrieved {fname}.")
        return fo


def process_file(fo):
    pass
