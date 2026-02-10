"""Database engine and session management.

This module provides the SQLAlchemy async engine, session factory,
and FastAPI dependency for database connections.
"""
from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class Engine:
    def __init__(self, database_uri: str) -> None:
        engine = create_async_engine(
            database_uri,
            echo=True,
            pool_pre_ping=True,
        )
        self.async_session_maker = async_sessionmaker(
            engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    @property
    def db_session(self):
        """Return the get_db dependency callable for FastAPI injection."""
        return self.get_db

    @classmethod
    def load_from_config(cls, database_uri: str) -> "Engine":
        """Create an Engine instance from the application configuration."""
        return cls(database_uri)

    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        """Provide an asynchronous database session.

        This function serves as a FastAPI dependency that creates and manages
        database sessions. It ensures proper cleanup after each request.

        Returns:
            AsyncSession: An active database session.

        """
        async with self.async_session_maker() as session:
            try:
                yield session
            finally:
                await session.close()

    async def test_db(self) -> None:
        """{...}."""
        async with self.async_session_maker() as session:
            result = await session.execute(text("SELECT 1"))
            if result.scalar() != 1:
                message = "Database test query failed"
                raise RuntimeError(message)
