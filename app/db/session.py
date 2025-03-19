import configparser
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')


from sqlalchemy.orm import class_mapper

dbname = config.get('db', 'dbname')
user = config.get('db', 'user')
password = config.get('db', 'pass')
host = config.get('db',"host")
driver = config.get('db',"driver")
port = config.get('db',"port")

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
DATABASE_URL = f"{driver}://{user}:{password}@{host}:{port}/{dbname}"
# DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@0.0.0.0:5430/{dbname}"
print('DATABASE URL = ',DATABASE_URL)

engine = create_async_engine(DATABASE_URL, echo=False)

def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_sessionmaker(bind=engine, expire_on_commit=False)() as session:
            try:
                # Явно не открываем транзакции, так как они уже есть в контексте
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()  # Откатываем сессию при ошибке
                raise e  # Поднимаем исключение дальше
            finally:
                await session.close()  # Закрываем сессию

    return wrapper

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    # here we can write some fields witch would exist 
    # in every table in database

    def to_dict(self) -> dict:
        """Универсальный метод для конвертации объекта SQLAlchemy в словарь"""
        # Получаем маппер для текущей модели
        columns = class_mapper(self.__class__).columns
        # Возвращаем словарь всех колонок и их значений
        return {column.key: getattr(self, column.key) for column in columns}
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'   
    
