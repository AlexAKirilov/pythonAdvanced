from datetime import datetime
from flask import jsonify, Flask, request
from sqlalchemy import create_engine, func, extract, desc
from sqlalchemy.orm import sessionmaker, selectinload
from models import Base, Books, Students, ReceivingBooks
from module_20.app import initialize_db

# Создание подключения к базе данных SQLite
engine = create_engine('sqlite:///library.db')
# Создание фабрики сессий для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Инициализация приложения Flask
app = Flask(__name__)


# Роут для получения всех книг
@app.route('/books', methods=['GET'])
def get_all_books():
    # Запрос всех книг из базы данных с предварительной загрузкой информации об авторе
    books = session.query(Books).options(selectinload(Books.author)).all()
    # Формирование списка книг для JSON-ответа
    book_list = [{"id": book.id, "name": book.name, "release_date": book.release_date, "author": {
        "id": book.author.id, "name": book.author.name, "surname": book.author.surname}} for book in books]
    session.close()
    # Возврат списка книг в формате JSON
    return jsonify(book_list)


# Роут для получения количества оставшихся в библиотеке книг по автору
@app.route('/books/count_by_author/<int:author_id>', methods=['GET'])
def get_book_count_by_author(author_id):
    # Запрос суммы количества книг по указанному автору
    book_count = session.query(func.sum(Books.count)).filter(Books.author_id == author_id).scalar()
    session.close()
    # Возврат количества книг в формате JSON
    return jsonify({"count": book_count})


# Роут для получения списка книг, которые студент не читал, но уже брал другие книги этого автора
@app.route('/books/unread_by_student/<int:student_id>', methods=['GET'])
def get_unread_books_by_student(student_id):
    # Запрос студента по идентификатору
    student = session.query(Students).get(student_id)
    if not student:
        return jsonify({"error": "Студент не найден"})

    # Запрос книг, авторы которых уже были у студента
    books_by_author = session.query(Books).filter(Books.author_id.in_(
        [book.author_id for book in student.books if book.date_of_return]
    )).all()

    # Формирование списка книг для JSON-ответа
    book_list = [{"id": book.id, "name": book.name, "release_date": book.release_date} for book in books_by_author]
    session.close()
    # Возврат списка книг в формате JSON
    return jsonify(book_list)


# Роут для получения среднего количества книг, которые студенты брали в текущем месяце
@app.route('/students/average_books_per_month', methods=['GET'])
def get_average_books_per_month():
    current_month = datetime.now().month
    # Запрос количества книг, выданных в текущем месяце
    books_count = session.query(func.count(ReceivingBooks.id)).filter(
        extract('month', ReceivingBooks.date_of_issue) == current_month).scalar()
    # Запрос общего количества студентов
    student_count = session.query(func.count(Students.id)).scalar()

    # Вычисление среднего количества книг на студента в месяц
    average_books_per_month = books_count / student_count if student_count else 0
    session.close()
    # Возврат среднего количества книг в формате JSON
    return jsonify({"average_books_per_month": average_books_per_month})


# Роут для получения самой популярной книги среди студентов с средним баллом больше 4.0
@app.route('/books/most_popular_among_high_achievers', methods=['GET'])
def get_most_popular_book_among_high_achievers():
    # Запрос студентов с средним баллом больше 4.0
    high_achievers = session.query(Students).filter(Students.average_score > 4.0).all()

    book_counts = {}
    # Подсчет количества заимствований книг студентами
    for student in high_achievers:
        for book in student.books:
            book_counts[book.id] = book_counts.get(book.id, 0) + 1

    # Нахождение идентификатора самой популярной книги
    most_popular_book_id = max(book_counts, key=book_counts.get) if book_counts else None
    # Запрос самой популярной книги по идентификатору
    most_popular_book = session.query(Books).filter(Books.id == most_popular_book_id).first()
    session.close()

    # Возврат информации о самой популярной книге в формате JSON
    return jsonify({"most_popular_book": {
        "id": most_popular_book.id,
        "name": most_popular_book.name,
        "release_date": most_popular_book.release_date
    }})


# Роут для получения ТОП-10 самых читающих студентов в этом году
@app.route('/students/top_readers', methods=['GET'])
def get_top_readers():
    # Запрос ТОП-10 студентов по количеству заимствованных книг в порядке убывания
    top_readers = session.query(Students).order_by(desc(Students.books_count)).limit(10).all()

    # Формирование списка студентов для JSON-ответа
    top_readers_list = [{"id": student.id, "name": student.name, "surname": student.surname,
                         "books_count": student.books_count} for student in top_readers]

    session.close()
    # Возврат списка ТОП-10 студентов в формате JSON
    return jsonify(top_readers_list)


# Роут для массовой вставки студентов из CSV
@app.route('/students/bulk_insert', methods=['POST'])
def bulk_insert_students():
    if 'file' not in request.files:
        return jsonify({"error": "Отсутствует файл"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Файл не выбран"})

    if file and file.filename.endswith('.csv'):
        try:
            # Чтение данных из файла CSV
            students_data = file.read().decode('utf-8').split('\n')
            students_data = [row.split(';') for row in students_data if row]
            students_dicts = []
            # Формирование списка словарей с данными студентов
            for row in students_data:
                student_dict = {
                    'name': row[0].strip(),
                    'surname': row[1].strip(),
                    'phone': row[2].strip(),
                    'email': row[3].strip(),
                    'average_score': float(row[4].strip()),
                    'scholarship': True if row[5].strip().lower() == 'true' else False
                }
                students_dicts.append(student_dict)

            # Массовая вставка данных студентов в базу данных
            session.bulk_insert_mappings(Students, students_dicts)
            session.commit()
            session.close()
            # Возврат сообщения об успешной вставке студентов в формате JSON
            return jsonify({"message": "Студенты успешно добавлены"})
        except Exception as e:
            session.rollback()
            session.close()
            # Возврат сообщения об ошибке в формате JSON
            return jsonify({"error": "Произошла ошибка при добавлении студентов: {}".format(str(e))})
    else:
        return jsonify({"error": "Недопустимый тип файла"})


# Запуск приложения Flask
if __name__ == '__main__':
    # Создание всех таблиц в базе данных, если они не существуют
    Base.metadata.create_all(engine)
    # Инициализация базы данных
    initialize_db()
    # Запуск сервера Flask в режиме отладки
    app.run(debug=True)
