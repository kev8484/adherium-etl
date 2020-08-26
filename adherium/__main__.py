""" Entrypoint for Adherium ETL
"""
import logging
import argparse
from datetime import datetime
from adherium.etl import get_file, process_file, put_file


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",  help="file name to process", default=None,
    )
    parser.add_argument(
        "-c", action="store_true", help="clean directory after processing"
    )
    parser.add_argument(
        "-p", action="store_true", help="print logs to console, otherwise write to file"
    )
    parser.add_argument(
        "--log",  help="log level", default="WARNING",
    )
    parser.add_argument(
        "-w", action="store_true", help="write processed file to local disk, do not upload"
    )
    return parser.parse(args)

def main(args):

    args = parse_args(args)
    log_level = args.log
    if log_level.upper() not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        raise ValueError(f"{log_level} not supported.")

    logging.basicConfig(

        filename=None if args.p else "adherium.log",
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        level=getattr(logging, log_level.upper()),
    )

    fo = get_file(remote_dir="INBOUND",
                  fname='2020-08-20_DailyMedicationUsage.csv')
    data_obj = process_file(fo=fo)
    put_file(fo=data_obj, remote_dir="QuickBase Sync/INBOUND/", fname="Test.csv")


if __name__ == '__main__':
    main()
