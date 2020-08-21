import logging
from base64 import decodebytes
from io import FileIO
from datetime import datetime

import paramiko
import pysftp

from config import Config


logger = logging.getLogger(__name__)
config = Config()

print(config.SFTP_HOSTNAME)
print(config.SFTP_USERNAME)
print(config.SFTP_HOSTKEY)


def get_file(remote_dir, fname):
    # connect
    cnopts = configure_hostkey(
        hostname=config.SFTP_HOSTNAME,
        hostkey=config.SFTP_HOSTKEY,
    )

    with pysftp.Connection(
        host=config.SFTP_HOSTNAME,
        username=config.SFTP_USERNAME,
        password=config.SFTP_PASSWORD,
        cnopts=cnopts,
    ) as sftp:
        logger.debug(
            f"Connection to {config.SFTP_HOSTNAME} successfully established."
        )
        print(
            f"Connection to {config.SFTP_HOSTNAME} successfully established.")
        # get file
        fo = FileIO()
        # fname = f"{datetime.today().strftime('%Y-%m-%d')}_DailyMedicationUsage.csv"
        sftp.getfo(f"{remote_dir}/{fname}", fo)
        logger.debug(f"Retrieved {fname}.")
        print(f"Retrieved {fname}.")
        return fo


def configure_hostkey(hostname, hostkey):
    keydata = str.encode(hostkey)
    key = paramiko.RSAKey(data=decodebytes(keydata))
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys.add(hostname, 'ssh-rsa', key)
    return cnopts


def process_file(fo):
    next(fo)  # skip header row
    rows = []
    for line in fo.readlines():
        cols = line.split(',')
        # get components
        sys_id = cols[1]
        med = cols[2]
        usage_count = cols[5].replace('*', '')
        overusage = cols[6]
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

    logger.debug(f"{len(rows)} rows of data found.")
    print(f"{len(rows)} rows of data found.")
    return rows
