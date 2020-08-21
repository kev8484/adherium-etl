import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """Set configuration vars from .env file."""

    # SFTP credentials
    SFTP_HOSTNAME = os.environ.get('SFTP_HOSTNAME')
    SFTP_USERNAME = os.environ.get('SFTP_USERNAME')
    SFTP_PASSWORD = os.environ.get('SFTP_PASSWORD')
