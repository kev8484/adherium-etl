""" Entrypoint for Adherium ETL
"""
import logging
from adherium.etl import get_file, process_file


def main():
    logging.basicConfig(
        filename="adherium.log",
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    fo = get_file(remote_dir="INBOUND",
                  fname='2020-08-20_DailyMedicationUsage.csv')
    data = process_file(fo=fo)
    print(data)


if __name__ == '__main__':
    main()
