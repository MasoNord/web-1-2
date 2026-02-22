from src.harmony_hound.main.config import load_database_config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

database_config = load_database_config()

DATABASE_URL = database_config.get_db_url()

engine = create_async_engine(url=DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                return await method(*args, **kwargs, session=session)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()
    return wrapper