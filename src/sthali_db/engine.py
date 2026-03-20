"""Database engine and session management.

This module provides the SQLAlchemy async engine, session factory,
and FastAPI dependency for database connections.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DBSession = AsyncSession


@asynccontextmanager
async def session_ctx(db_session_factory, db_session: AsyncSession | None = None):
    """Resolve a session from a FastAPI dependency or use the provided session.

    Args:
        db_session_factory: Callable returning an async generator of sessions.
        db_session: A concrete AsyncSession when injected by FastAPI.
    """
    if isinstance(db_session, AsyncSession):
        yield db_session
        return

    session_gen = db_session_factory()
    session = await anext(session_gen)
    try:
        yield session
    finally:
        await session_gen.aclose()


class Engine:
    """{...}."""

    def __init__(self, database_uri: str) -> None:
        """{...}."""
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

    @classmethod
    def load_from_config(cls, database_uri: str) -> "Engine":
        """Create an Engine instance from the application configuration."""
        return cls(database_uri)

    async def db_session(self) -> AsyncGenerator[AsyncSession, None]:
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
