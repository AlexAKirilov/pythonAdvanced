from flask import Flask
from datetime import datetime

app = Flask(__name__)

weekdays_tuple = ('понедельника', 'вторника', 'среды', 'четверга', 'пятницы', 'субботы', 'воскресения')

@app.route('/hello-world/<string:username>')
def hello_world(username: str):
    weekday = datetime.today().weekday()
    if weekday == 0 or weekday == 1 or weekday == 3 or weekday == 6:
        greeting_word = 'Хорошего'
    else:
        greeting_word = 'Хорошей'
    return f'Привет, {username}. {greeting_word} {weekdays_tuple[weekday]}!'

if __name__ == '__main__':
    app.run(debug=True)