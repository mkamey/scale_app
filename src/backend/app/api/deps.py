from typing import AsyncGenerator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from app.database import get_db
from app.core.config import settings
from app.core.security import verify_password
from app.crud.patient import patient
from app.models import Patient

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Optional[Patient]:
    """
    現在のユーザー（医師）を取得する依存関係
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="認証情報が無効です",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await patient.get(db, user_id)
    if user is None:
        raise credentials_exception
    return user

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    データベースセッションの依存関係
    """
    async with get_db() as session:
        yield session

def get_pagination_params(
    skip: int = 0,
    limit: int = 10
) -> tuple[int, int]:
    """
    ページネーションパラメータの依存関係
    """
    return skip, min(limit, 100)

async def validate_assessment_exists(
    assessment_id: str,
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    検査の存在確認の依存関係
    """
    from app.crud.assessment import assessment
    if not await assessment.exists(db, assessment_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された検査が見つかりません"
        )

async def validate_patient_exists(
    patient_id: str,
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    患者の存在確認の依存関係
    """
    if not await patient.exists(db, patient_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された患者が見つかりません"
        )

async def validate_result_exists(
    result_id: str,
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    検査結果の存在確認の依存関係
    """
    from app.crud.result import assessment_result
    if not await assessment_result.exists(db, result_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された検査結果が見つかりません"
        )