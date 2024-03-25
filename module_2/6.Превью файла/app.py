from flask import Flask
import os

app = Flask(__name__)


@app.route('/head_file/<int:size>/<path:relative_path>')
def head_file(size: int, relative_path):
    print(relative_path)
    if os.path.exists(f'{relative_path}'):
        with open(f'{relative_path}', 'r') as file:
            head = file.read(int(size))
        abs_path = os.path.abspath(relative_path)
        return (f'<strong>{abs_path}</strong> {len(head)} <br>'
                f'{head}')
    else:
        return 'not exists'

if __name__=='__main__':
    app.run(debug=True, port=5555)