import configparser
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')




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

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    # here we can write some fields witch would exist 
    # in every table in database
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'