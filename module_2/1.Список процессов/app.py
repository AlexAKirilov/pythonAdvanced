import pandas as pd


def processors(file_path):
    df = pd.read_table(file_path, delimiter='\s+', usecols=[5])
    summary = df['RSS'].sum()
    size_index = 0

    while summary >= 1024:
        summary //= 1024
        size_index += 1

    sizing_name = {0: 'Б', 1: 'Кб', 2: 'Мб', 3: 'Гб', 4: 'Тб'}

    size_unit_name = sizing_name[size_index]

    return f"{summary} {size_unit_name}"


if __name__ == '__main__':
    file_path = input()
    print(processors(file_path))