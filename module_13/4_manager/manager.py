import sqlite3

sql_request_salary_worker = """SELECT salary FROM table_effective_manager WHERE name = ?"""
sql_request_update_salary = """UPDATE table_effective_manager SET salary = ? WHERE name = ?"""
sql_request_delete_worker = """DELETE FROM table_effective_manager WHERE name = ?"""


def get_salary(cursor: sqlite3.Cursor, name: str) -> float:
    """Получить зарплату сотрудника по имени."""
    cursor.execute(sql_request_salary_worker, (name,))
    salary = cursor.fetchone()[0]
    return salary


def ivan_sovin_the_most_effective(cursor: sqlite3.Cursor, name: str) -> None:
    """Повысить зарплату сотрудника или уволить его, если зарплата станет выше, чем у Ивана Совина."""
    salary_ivan_sovin = get_salary(cursor, "Иван Совин")
    salary_worker = get_salary(cursor, name)

    print(f"Зарплата сотрудника {name} составляет: {salary_worker}")

    new_salary = salary_worker * 1.10

    if new_salary > salary_ivan_sovin:
        cursor.execute(sql_request_delete_worker, (name,))
        print(f"Зарплата оказалась выше, чем у Ивана Совина. Сотрудник {name} уволен.")
    else:
        cursor.execute(sql_request_update_salary, (new_salary, name))
        print(f"Зарплата сотрудника {name} была повышена до: {new_salary}")


if __name__ == "__main__":
    with sqlite3.connect("../homework.db") as conn:
        cursor = conn.cursor()
        name = input("Введите имя сотрудника:\n")
        ivan_sovin_the_most_effective(cursor, name)