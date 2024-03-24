import sys


def get_mean_size(data):
    total_size = 0
    file_count = 0

    lines = data.split('\n')
    for line in lines:
        if line:
            # Разделение строки по пробелам и выбор индекса, содержащего размер файла
            parts = line.split()
            if len(parts) >= 5:
                try:
                    size = int(parts[4])
                    total_size += size
                    file_count += 1
                except ValueError:
                    pass

    if file_count == 0:
        return "No files or unable to get file sizes"

    mean_size = total_size / file_count
    return mean_size


if __name__ == "__main__":
    data = sys.stdin.read()
    mean_size = get_mean_size(data)
    print(mean_size)
