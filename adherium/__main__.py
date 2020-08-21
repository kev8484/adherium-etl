""" Entrypoint for Adherium ETL
"""
import logging


def main():
    logging.basicConfig(
        filename="adherium.log",
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )


if __name__ == '__main__':
    main()
