from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

async_engine = create_async_engine("postgresql+psycopg://postgres:penis@0.0.0.0:5430/wfstats")


SessionAsync = async_sessionmaker(async_engine)


def get_async_db_session() -> SessionAsync:
    return SessionAsync