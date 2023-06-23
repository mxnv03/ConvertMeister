from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://user:123456789@db:5432/converter')

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Определение базовой модели
Base = declarative_base()


# Определение модели файла
class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    token = Column(String)
    status = Column(String)


# Определение модели имени файла
class FileName(Base):
    __tablename__ = 'filenames'
    id = Column(Integer, primary_key=True)
    token = Column(String)
    name = Column(String)


# Добавление файла
def add_file(status, token):
    file = File(token=token, status=status)
    session.add(file)
    session.commit()


# Добавление имени файла
def add_name(token, name):
    filename = FileName(token=token, name=name)
    session.add(filename)
    session.commit()


# Получение оригинального имени файла
def get_orig(token):
    filename = session.query(FileName).filter_by(token=token).first()
    if filename:
        return filename.name
    else:
        return None

