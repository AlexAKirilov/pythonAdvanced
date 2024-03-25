from flask import Flask
from collections import defaultdict

app = Flask(__name__)
storage = defaultdict(lambda: defaultdict(int))

@app.route('/add/<date>/<int:expense>')
def add_expense(date, expense):
    year = int(date[:4])
    month = int(date[4:6])
    storage.setdefault(year, defaultdict(int)).setdefault(month, 0)
    storage[year][month] += expense
    return 'Expense added successfully'

@app.route('/calculate/<int:year>')
def calculate_year(year):
    total_expense = sum(storage[year].values())
    return f'Total expenses for year {year}: {total_expense}'

@app.route('/calculate/<int:year>/<int:month>')
def calculate_month(year, month):
    expense = storage[year][month]
    return f'Expenses for {month}/{year}: {expense}'

if __name__ == '__main__':
    app.run(debug=True)
