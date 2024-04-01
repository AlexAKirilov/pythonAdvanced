from flask import Flask

app = Flask(__name__)


@app.route('/max_number/<path:numbers>')
def max_number(numbers):
    list_of_numbers = numbers.split('/')
    try:
        list_of_numbers = [float(x) for x in list_of_numbers]
        max_num = max(list_of_numbers)
        try:
            if max_num % 1 == 0:
                max_num = int(max_num)
            else:
                pass
        except:
            max_num = max_num
        return f'<i>{str(max_num)}</i>'
    except:
        return 'Error. Invalid argument type on input'


if __name__ == '__main__':
    app.run(debug=True)
