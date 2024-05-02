import sqlite3
import csv

SQL_DELETE_REQUEST = """
DELETE FROM table_fees 
WHERE truck_number = ? 
    AND timestamp = ?;
"""

def delete_wrong_fees(cursor: sqlite3.Cursor, wrong_fees_file: str) -> None:
    with open(wrong_fees_file) as csvfile:
        wrong_fees_reader = csv.reader(csvfile, delimiter=',')
        for row in wrong_fees_reader:
            cursor.execute(SQL_DELETE_REQUEST, (row[0], row[1]))

if __name__ == "__main__":
    with sqlite3.connect("../homework.db") as conn:
        cursor = conn.cursor()
        delete_wrong_fees(cursor, "../wrong_fees.csv")