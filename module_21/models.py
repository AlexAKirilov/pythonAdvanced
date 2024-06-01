from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, Float, Boolean, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Создание базового класса для декларативной базы данных
Base = declarative_base()


# Таблица книг в библиотеке
class Books(Base):
    __tablename__ = 'books'

    # Поля таблицы
    id = Column(Integer, primary_key=True)  # Первичный ключ
    name = Column(String, nullable=False)  # Название книги
    count = Column(Integer, default=1)  # Количество экземпляров книги в библиотеке
    release_date = Column(Date, nullable=False)  # Дата выпуска книги
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)  # Внешний ключ на таблицу авторов
    author = relationship('Authors', backref='books')  # Связь с таблицей авторов
    receiving_books = relationship('ReceivingBooks', backref='book',
                                   cascade='all, delete-orphan')  # Связь с таблицей выдачи книг


# Таблица авторов
class Authors(Base):
    __tablename__ = 'authors'

    # Поля таблицы
    id = Column(Integer, primary_key=True)  # Первичный ключ
    name = Column(String, nullable=False)  # Имя автора
    surname = Column(String, nullable=False)  # Фамилия автора


# Таблица читателей (студентов)
class Students(Base):
    __tablename__ = 'students'

    # Поля таблицы
    id = Column(Integer, primary_key=True)  # Первичный ключ
    name = Column(String, nullable=False)  # Имя студента
    surname = Column(String, nullable=False)  # Фамилия студента
    phone = Column(String, nullable=False)  # Номер телефона студента
    email = Column(String, nullable=False)  # Электронная почта студента
    average_score = Column(Float, nullable=False)  # Средний балл студента
    scholarship = Column(Boolean, nullable=False)  # Наличие стипендии у студента
    received_books = relationship('ReceivingBooks', backref='student')  # Связь с таблицей выдачи книг
    books = association_proxy('received_books', 'book')  # Прокси-ассоциация для доступа к книгам через выдачи


# Таблица выдачи книг студентам
class ReceivingBooks(Base):
    __tablename__ = 'receiving_books'

    # Поля таблицы
    id = Column(Integer, primary_key=True)  # Первичный ключ
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)  # Внешний ключ на таблицу книг
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)  # Внешний ключ на таблицу студентов
    date_of_issue = Column(Date, nullable=False)  # Дата выдачи книги
    date_of_return = Column(Date)  # Дата возврата книги

    # Гибридное свойство для вычисления количества дней с момента выдачи книги до возврата или текущей даты
    @hybrid_property
    def count_date_with_book(self):
        if self.date_of_return:
            return (self.date_of_return - self.date_of_issue).days  # Количество дней между выдачей и возвратом
        else:
            return (datetime.now() - self.date_of_issue).days  # Количество дней между выдачей и текущей датой
