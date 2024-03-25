import re
import sys


def decrypt(encrypted_data):
    while '..' in encrypted_data:
        encrypted_data = re.sub(r'(\w{1}|\W{1})\.{2}', '', encrypted_data, count=1)
    while '.' in encrypted_data:
        encrypted_data = encrypted_data.replace('.', '')
    return encrypted_data


if __name__ == '__main__':
    encrypted_data = sys.stdin.read()
    print(decrypt(encrypted_data))