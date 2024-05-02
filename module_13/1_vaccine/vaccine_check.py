import sqlite3

SQL_REQUEST = """
SELECT * 
FROM table_truck_with_vaccine 
WHERE temperature_in_celsius NOT BETWEEN 16 AND 20 
    AND truck_number = ? 
ORDER BY timestamp;
"""

def check_if_vaccine_has_spoiled(cursor: sqlite3.Cursor, truck_number: str) -> bool:
    cursor.execute(SQL_REQUEST, (truck_number,))
    result = cursor.fetchall()
    print(result)
    return len(result) >= 3

if __name__ == "__main__":
    with sqlite3.connect("../homework.db") as conn:
        cursor = conn.cursor()
        truck_number = input("Введите номер грузовика:\n")
        if check_if_vaccine_has_spoiled(cursor, truck_number):
            print("Вакцина испорчена")
        else:
            print("Вакцина в нормальном состоянии")