from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from contextlib import asynccontextmanager
from config import Config

class DatabaseManager:
    _instance = None
    _engine = None
    _session_local = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        try:
            config = Config()  # Artık singleton olduğu için güvenli
            self._engine = create_async_engine(
                f"postgresql+asyncpg://{config.postgres_user}:{config.postgres_password}@{config.postgres_host}:{config.postgres_port}/{config.postgres_database}",
                echo=False,  # Set to True for SQL logging
                pool_size=20,
                max_overflow=0
            )
            self._session_local = async_sessionmaker(
                self._engine, 
                class_=AsyncSession, 
                expire_on_commit=False
            )
        except Exception as e:
            print(f"Error loading config: {e}")
            exit(1)
    
    @property
    def session_local(self):
        return self._session_local
    
    @property
    def engine(self):
        return self._engine

# Singleton instance'ını oluştur
db_manager = DatabaseManager()

# Dependency for getting DB session
async def get_db_session() -> AsyncSession:
    async with db_manager.session_local() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()