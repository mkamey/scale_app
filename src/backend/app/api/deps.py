from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException, status, Query

DATABASE_URL = "sqlite+aiosqlite:///./test.db"  # 例としてSQLiteを使用

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    データベースセッションの依存関係
    """
    async for session in get_db():
        yield session

async def validate_patient_exists(patient_id: int, db: AsyncSession):
    """
    患者が存在するか確認する
    """
    patient = await db.execute(select(Patient).where(Patient.id == patient_id))
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

async def validate_assessment_exists(assessment_id: int, db: AsyncSession):
    """
    評価が存在するか確認する
    """
    assessment = await db.execute(select(Assessment).where(Assessment.id == assessment_id))
    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )

async def validate_result_exists(result_id: int, db: AsyncSession):
    """
    結果が存在するか確認する
    """
    result = await db.execute(select(Result).where(Result.id == result_id))
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found"
        )

def get_pagination_params(
    skip: int = Query(0, description="スキップするアイテムの数"),
    limit: int = Query(10, description="取得するアイテムの最大数"),
):
    return {"skip": skip, "limit": limit}