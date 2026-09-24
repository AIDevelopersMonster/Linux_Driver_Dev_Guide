import os
import re

# Папка, в которой хранятся .rst файлы
SOURCE_DIR = 'source'

# Регулярное выражение для удаления emoji и не-ASCII символов, кроме кириллицы
def remove_emojis(text):
    return re.sub(r'[^\x00-\x7Fа-яА-ЯёЁ\s.,;:\-_/()\[\]{}!?\'"=+*#@&%<>|\\]', '', text)

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    cleaned = remove_emojis(content)
    if content != cleaned:
        print(f"Cleaned: {filepath}")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned)

# Рекурсивный обход
for root, dirs, files in os.walk(SOURCE_DIR):
    for file in files:
        if file.endswith('.rst'):
            full_path = os.path.join(root, file)
            process_file(full_path)
