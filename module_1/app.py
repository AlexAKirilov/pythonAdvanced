import os
import random
import datetime
import re
from datetime import timedelta

from flask import Flask

app = Flask(__name__)


@app.route('/hello_world')
def helloWorld():
    return 'Привет, мир!'


@app.route('/cars')
def cars():
    return ', '.join(cars)


cars = ['Chevrolet', 'Renault', 'Ford', 'Lada']


@app.route('/cats')
def cats():
    return random.choice(cats)


cats = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']


@app.route('/get_time/now')
def getTime():
    current_time = datetime.datetime.now()
    return f"Точное время: {current_time}"


@app.route('/get_time/future')
def getFutureTime():
    current_time_after_hour = datetime.datetime.now() + timedelta(hours=1)
    return f"Точное время через час будет {current_time_after_hour}"


BASE_DIR = os.path.dirname(os.path.abspath('war_and_peace.txt'))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')


def get_words(BOOK_FILE):
    with open(BOOK_FILE) as book:
        book = book.read()
    words = re.findall(r"\w+", book)
    return words


words = get_words(BOOK_FILE)


@app.route('/get_random_word')
def random_word():
    return random.choice(words)


count = 0


@app.route('/counter')
def counter():
    global count
    count += 1
    return str(count)
