""" Entrypoint for Adherium ETL
"""
import logging
from adherium.etl import get_file, process_file, put_file


def main():
    logging.basicConfig(
        filename="adherium.log",
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        # level=logging.DEBUG,
    )

    fo = get_file(remote_dir="INBOUND",
                  fname='2020-08-20_DailyMedicationUsage.csv')
    data_obj = process_file(fo=fo)
    put_file(fo=data_obj, remote_dir="QuickBase Sync/INBOUND/", fname="Test.csv")


if __name__ == '__main__':
    main()
