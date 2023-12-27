"""Handles the database for the data readings web site"""
import sqlite3
from typing import Any, List


class SQLite3db:
    """Encapsulates the SQLite3 operations"""

    CREATE_SQL = """
    CREATE TABLE IF NOT EXISTS data_readings
    (tvoc INT NOT NULL, 
    eco2 INT NOT NULL,
    date DATETIME NOT NULL);
    """

    def __init__(self, db_name):
        """Creates the database"""
        self.db_name = db_name
        with sqlite3.connect(
            self.db_name,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        ) as conn:
            cur = conn.cursor()
            cur.execute(self.CREATE_SQL)
            conn.commit()

    def store_data_readings(self, tvoc, eco2):
        """Stores a data readings in the DB

        Args:
            tvoc (int): the tvoc data
            eco2 (int): the eco2 data

        Returns:
            int: the number of rows affected (should be 2)
        """
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO data_readings (tvoc, eco2, date) VALUES (?,?,DATETIME('now'))",
                (tvoc, eco2,),
            )
            conn.commit()
            return cur.rowcount

    def all_data_readings(self):
        """Returns all tvoc and eco2 data in the DB

        Returns:
            List: a list of tuples
        """
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(
                """SELECT *
                   FROM data_readings
                   ORDER BY date DESC;"""
            )
            return cur.fetchall()

    def max_tvoc(self):
        """
        Returns max TVOC
        """
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(
                """SELECT MAX(tvoc), date
                   FROM data_readings;"""
            )
            return cur.fetchall()
    
    def min_tvoc(self):
        """
        Returns min TVOC and date
        """
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(
                """SELECT MIN(tvoc), date
                   FROM data_readings;"""
            )
            return cur.fetchall()

    def max_eco2(self):
        """
        Returns max eCO2
        """
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(
                """SELECT MAX(eco2), date
                   FROM data_readings;"""
            )
            return cur.fetchall()

    def min_eco2(self):
        """
        Returns min eCO2
        """
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(
                """SELECT MIN(eco2), date
                   FROM data_readings;"""
            )
            return cur.fetchall()

    def latest(self):
        """
        Returns the latest data
        """
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(
                """SELECT *
                   FROM data_readings
                   ORDER BY date DESC LIMIT 1;"""
            )
            return cur.fetchall()

    def paged(self, paged):
        """
        Returns 20 relative to the page number.
        """
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(
                """SELECT *
                   FROM data_readings
                   ORDER BY date DESC
                   LIMIT 20 OFFSET (?);""",
                   (paged,),
            )
            return cur.fetchall()