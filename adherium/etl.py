import logging
import csv
from io import BytesIO, StringIO

import pysftp

from config import Config


logger = logging.getLogger(__name__)
config = Config()


def get_file(remote_dir, fname):

    with pysftp.Connection(
        host=config.SFTP_HOSTNAME,
        username=config.SFTP_USERNAME,
        password=config.SFTP_PASSWORD,
    ) as sftp:
        logger.debug(
            f"Connection to {config.SFTP_HOSTNAME} successfully established."
        )
        # get file
        fo = BytesIO()
        # fname = f"{datetime.today().strftime('%Y-%m-%d')}_DailyMedicationUsage.csv"
        sftp.getfo(f"{remote_dir}/{fname}", fo)
        logger.debug(f"Retrieved {fname}.")
        return fo.getvalue()  # return byte string


def process_file(fo):
    rows = []
    with StringIO(fo.decode()) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",", quotechar='"')
        next(csvreader)  # skip header row
        for row in csvreader:
            # get components
            sys_id = row[1]
            med = row[2]
            usage_count = row[5].replace('*', '')
            overusage = row[6]
            # all registered patients are listed in the file by default,
            # so ignore rows with no new data
            if usage_count == 'N/A' or usage_count == 'ND':
                continue
            else:
                # store fresh data
                rows.append({
                    "System ID": sys_id,
                    'Medication': med,
                    "Usage Count": usage_count,
                    "Overusage": overusage
                })
    # fo.close()  # close input stream buffer
    logger.debug(f"{len(rows)} rows of data found.")
    output = StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=['System ID', 'Medication', 'Usage Count', 'Overusage']
    )
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

    return output


def put_file(fo, remote_dir, fname, cleanup_path=None):
    # connect
    with pysftp.Connection(
        host=config.SFTP_HOSTNAME,
        username=config.SFTP_USERNAME,
        password=config.SFTP_PASSWORD,
    ) as sftp:
        # put file
        with sftp.cd(remote_dir):
            fo.seek(0)
            sftp.putfo(fo, remotepath=fname)
            logger.debug(f"Uploaded {fname}.")

        # clean up INBOUND directory
        if cleanup_path is not None and sftp.isfile(cleanup_path):
            sftp.remove(cleanup_path)
            logger.debug(f"Removed file {cleanup_path}.")
