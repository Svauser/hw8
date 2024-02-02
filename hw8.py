import sqlite3

conn = sqlite3.connect('school_database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS countries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL
    )
''')


cursor.executemany('INSERT INTO countries (title) VALUES (?)', [('Kyrgyzstan',), ('Germany',), ('China',)])
conn.commit()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        area REAL DEFAULT 0,
        country_id INTEGER,
        FOREIGN KEY (country_id) REFERENCES countries (id)
    )
''')


cities_data = [('Bishkek', 120, 1), ('Berlin', 891.8, 2), ('Beijing', 16410.54, 3),
               ('Osh', 182, 1), ('Moscow', 2561, 0), ('Tokyo', 2187, 0), ('New York', 468.9, 0)]
cursor.executemany('INSERT INTO cities (title, area, country_id) VALUES (?, ?, ?)', cities_data)
conn.commit()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        city_id INTEGER,
        FOREIGN KEY (city_id) REFERENCES cities (id)
    )
''')


students_data = [
    ('Михаил', 'Орлов', 1),
    ('Тилек', 'Курманов', 2),
    ('Алексей', 'Алексеев', 3),
    ('Айсулу', 'Кенешбекова', 4),
    ('Алиса', 'Ким', 5),
    ('Мирон', 'Янович', 6),
    ('Алмаз', 'Малкович', 8),
    ('Эркин', 'Токонов', 9),
    ('Болот', 'Саяков', 10),
    ('Гуля', 'Иманова', 11),
    ('Дмитрий', 'Смирнов', 12),
    ('Феликс', 'Кжелберг', 7),
    ('Айжан', 'Жамаева', 13),
    ('Азамат', 'Аманов', 14),
    ('Канат', 'Смалбеков', 15),

]
cursor.executemany('INSERT INTO students (first_name, last_name, city_id) VALUES (?, ?, ?)', students_data)
conn.commit()


while True:

    cursor.execute('SELECT id, title FROM cities')
    cities = cursor.fetchall()
    print("Вы можете отобразить список учеников по выбранному id города из перечня городов ниже, для выхода из программы введите 0:")
    for city in cities:
        print(f"{city[0]}. {city[1]}")

    selected_city_id = int(input("Введите id города: "))
    if selected_city_id == 0:
        break


    cursor.execute('''
        SELECT s.first_name, s.last_name, c.title, c.area
        FROM students s
        JOIN cities c ON s.city_id = c.id
        WHERE c.id = ?
    ''', (selected_city_id,))
    students_info = cursor.fetchall()

    if students_info:
        print(f"\nУченики в городе {cities[selected_city_id-1][1]}:")
        for student in students_info:
            print(f"Имя: {student[0]}, Фамилия: {student[1]}, Страна: {student[2]}, Город: {cities[selected_city_id-1][1]}, Площадь города: {student[3]}")
    else:
        print("В выбранном городе нет учеников.")

conn.close()