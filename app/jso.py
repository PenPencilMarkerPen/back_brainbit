import json
import random
import time

count = 0
data = []   

while count < 10:
    current_time = str(int(time.time()))  # Получаем текущее время в формате UNIX timestamp
    count += 1

    # Генерируем случайные значения для positive и negative
    positive_count = random.randint(1, 100)
    negative_count = 100 - positive_count
    
    # Создаем словарь для каждой итерации и добавляем его в список
    data.append({
        "date": current_time,
        "positive": str(positive_count),
        "negative": str(negative_count)
    })

# Записываем JSON данные в файл
with open('data.json', 'w') as file:  # Используем 'w' для записи новых данных, а не 'a' для добавления к существующему файлу
    json.dump(data, file)

with open('data.json', 'r') as file:
    data = json.load(file)
    print(data)