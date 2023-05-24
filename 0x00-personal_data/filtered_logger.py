#!/usr/bin/env python3
"""
filtered_logger module
"""
import os
import re
import logging
import mysql.connector
from typing import List


patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str,
) -> str:
    """Filters a log line."""
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


def get_logger() -> logging.Logger:
    """Returns a logger object"""
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database"""
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )
    return connection


def main():
    """Main function"""
    fields = [
        "name", "email", "phone", "ssn",
        "password", "ip", "last_login", "user_agent"
    ]
    info_logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute("SELECT {} FROM users".format(",".join(fields)))
        rows = cursor.fetchall()
        for row in rows:
            log_data = "; ".join(
                "{}={}".format(field, value)
                for field, value in zip(fields, row)
            )
            info_logger.info(log_data)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter clas
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formats a LogRecord."""
        msg = super(RedactingFormatter, self).format(record)
        txt = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt


if __name__ == "__main__":
    main()
