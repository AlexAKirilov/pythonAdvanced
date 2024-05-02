import requests
import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor

def fetch_character_data(url):
    """Загружает данные о персонаже по URL."""
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            'name': data.get('name', 'Unknown'),
            'age': data.get('birth_year', 'Unknown'),
            'gender': data.get('gender', 'Unknown')
        }
    else:
        return None

def persist_character_data(character):
    """Сохраняет данные персонажа в базу данных."""
    if character:
        conn = sqlite3.connect('characters.db')
        c = conn.cursor()
        c.execute("""
            INSERT INTO characters (name, age, gender)
            VALUES (?, ?, ?)
        """, (character['name'], character['age'], character['gender']))
        conn.commit()
        conn.close()

def initialize_database():
    """Инициализирует базу данных, если она еще не существует."""
    conn = sqlite3.connect('characters.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS characters (
            name TEXT,
            age TEXT,
            gender TEXT
        )
    """)
    conn.commit()
    conn.close()

def download_characters():
    """Загружает данные о первых 20 персонажах из Star Wars API."""
    character_urls = [f'https://swapi.dev/api/people/{i}/' for i in range(1, 21)]
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_character = {executor.submit(fetch_character_data, url): url for url in character_urls}
        for future in future_to_character:
            character = future.result()
            persist_character_data(character)
    return [character for character in future_to_character.values() if character is not None]

def time_function(func):
    """Измеряет время выполнения функции."""
    start_time = time.time()
    result = func()
    end_time = time.time()
    print(f"Total runtime is {end_time - start_time} seconds")
    return result

def main():
    initialize_database()
    characters = time_function(download_characters)
    print(f"Downloaded {len(characters)} characters")

if __name__ == '__main__':
    main()