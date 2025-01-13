from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool
import os
from typing import Generator

# データベースURLの設定
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./scale_app.db"  # デフォルトはSQLite
)

# エンジンの作成
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=NullPool,
    echo=True  # SQLログを出力（開発環境用）
)

# 非同期セッションの設定
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# モデルのベースクラス
Base = declarative_base()

async def get_db() -> Generator[AsyncSession, None, None]:
    """
    データベースセッションの依存関係
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db() -> None:
    """
    データベースの初期化
    """
    async with engine.begin() as conn:
        # 開発環境でのみ使用（本番環境ではマイグレーションを使用）
        await conn.run_sync(Base.metadata.create_all)

async def close_db() -> None:
    """
    データベース接続のクリーンアップ
    """
    await engine.dispose()