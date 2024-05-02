from datetime import datetime, timedelta
import sqlite3

# Constants
COUNT_DAYS = 366
COUNT_EMPLOYEES_PER_DAY = 10
COUNT_EMPLOYEES = 366
WORKING_DAYS_PER_EMPLOYEE = COUNT_DAYS * COUNT_EMPLOYEES_PER_DAY // COUNT_EMPLOYEES
WEEK_DAYS = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
SPORTS = ['футбол', "хоккей", "шахматы", "SUP сёрфинг", "бокс", "Dota2", "шах-бокс"]

# SQL queries
SQL_DELETE_ALL_ROWS = """
    DELETE FROM table_friendship_schedule
"""

SQL_GET_ALL_EMPLOYEES = """
    SELECT id, preferable_sport FROM table_friendship_employees
"""

SQL_INSERT_EMPLOYEE_SCHEDULE = """
    INSERT INTO table_friendship_schedule (employee_id, date)
        VALUES (?,?)
"""


def main():
    with sqlite3.connect("../homework.db") as conn:
        cursor = conn.cursor()
        cursor.execute(SQL_DELETE_ALL_ROWS)

        employees = cursor.execute(SQL_GET_ALL_EMPLOYEES).fetchall()

        working_days_per_employee = {employee[0]: 0 for employee in employees}
        daily_employees_count = {datetime(2020, 1, 1) + timedelta(days=i): 0 for i in range(COUNT_DAYS)}

        for day, _ in daily_employees_count.items():
            for employee_id, sport in employees:
                if WEEK_DAYS[day.weekday()] == WEEK_DAYS[SPORTS.index(sport)]:
                    continue
                if working_days_per_employee[employee_id] < WORKING_DAYS_PER_EMPLOYEE:
                    cursor.execute(SQL_INSERT_EMPLOYEE_SCHEDULE, (employee_id, day.strftime("%Y-%m-%d")))
                    working_days_per_employee[employee_id] += 1
                    daily_employees_count[day] += 1
                    if daily_employees_count[day] == COUNT_EMPLOYEES_PER_DAY:
                        break


if __name__ == "__main__":
    main()