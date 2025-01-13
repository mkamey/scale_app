from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.api.deps import (
    get_db_session,
    get_pagination_params,
    validate_assessment_exists
)
from app.crud.assessment import assessment
from app.schemas.assessment import (
    AssessmentCreate,
    AssessmentUpdate,
    AssessmentResponse,
    QuestionCreate,
    OptionCreate
)
from app.schemas.base import PaginatedResponse
from app.models import Question, Option

router = APIRouter()

@router.post(
    "/",
    response_model=AssessmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="検査の新規作成"
)
async def create_assessment(
    *,
    db: AsyncSession = Depends(get_db_session),
    assessment_in: AssessmentCreate
) -> AssessmentResponse:
    """
    新しい検査を作成します。

    - **name**: 検査名（必須）
    - **type**: 検査タイプ（必須）
    - **description**: 検査の説明
    - **cutoff**: カットオフ値（必須）
    - **max_score**: 最大スコア（必須）
    - **questions**: 質問リスト（必須）
    - **options**: 選択肢リスト（必須）
    """
    return await assessment.create(db, obj_in=assessment_in)

@router.get(
    "/{assessment_id}",
    response_model=AssessmentResponse,
    summary="検査情報の取得"
)
async def get_assessment(
    *,
    db: AsyncSession = Depends(get_db_session),
    assessment_id: UUID
) -> AssessmentResponse:
    """
    指定されたIDの検査情報を取得します。

    - **assessment_id**: 検査のID（必須）
    """
    await validate_assessment_exists(assessment_id, db)
    result = await assessment.get_with_questions(db, assessment_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された検査が見つかりません"
        )
    return result

@router.put(
    "/{assessment_id}",
    response_model=AssessmentResponse,
    summary="検査情報の更新"
)
async def update_assessment(
    *,
    db: AsyncSession = Depends(get_db_session),
    assessment_id: UUID,
    assessment_in: AssessmentUpdate
) -> AssessmentResponse:
    """
    指定されたIDの検査情報を更新します。

    - **assessment_id**: 検査のID（必須）
    - **name**: 検査名
    - **type**: 検査タイプ
    - **description**: 検査の説明
    - **cutoff**: カットオフ値
    - **max_score**: 最大スコア
    """
    await validate_assessment_exists(assessment_id, db)
    db_obj = await assessment.get(db, assessment_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された検査が見つかりません"
        )
    return await assessment.update(db, db_obj=db_obj, obj_in=assessment_in)

@router.delete(
    "/{assessment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="検査の削除"
)
async def delete_assessment(
    *,
    db: AsyncSession = Depends(get_db_session),
    assessment_id: UUID
) -> None:
    """
    指定されたIDの検査を削除します。

    - **assessment_id**: 検査のID（必須）
    """
    await validate_assessment_exists(assessment_id, db)
    await assessment.remove(db, id=assessment_id)

@router.get(
    "/",
    response_model=PaginatedResponse,
    summary="検査一覧の取得"
)
async def list_assessments(
    *,
    db: AsyncSession = Depends(get_db_session),
    pagination: tuple[int, int] = Depends(get_pagination_params)
) -> PaginatedResponse:
    """
    検査の一覧を取得します。

    - **skip**: スキップする件数
    - **limit**: 取得する最大件数
    """
    skip, limit = pagination
    assessments = await assessment.get_multi(db, skip=skip, limit=limit)
    total = len(assessments)  # 本来はcount queryを使用すべき
    return PaginatedResponse(
        total=total,
        page=skip // limit + 1,
        per_page=limit,
        items=assessments,
        has_next=total == limit,
        has_prev=skip > 0
    )

@router.post(
    "/{assessment_id}/questions",
    response_model=AssessmentResponse,
    summary="質問の追加"
)
async def add_question(
    *,
    db: AsyncSession = Depends(get_db_session),
    assessment_id: UUID,
    question_in: QuestionCreate
) -> AssessmentResponse:
    """
    指定された検査に質問を追加します。

    - **assessment_id**: 検査のID（必須）
    - **text**: 質問文（必須）
    - **order**: 表示順序（必須）
    """
    await validate_assessment_exists(assessment_id, db)
    question = Question(**question_in.model_dump())
    await assessment.add_question(db, assessment_id, question)
    return await assessment.get_with_questions(db, assessment_id)

@router.post(
    "/{assessment_id}/options",
    response_model=AssessmentResponse,
    summary="選択肢の追加"
)
async def add_option(
    *,
    db: AsyncSession = Depends(get_db_session),
    assessment_id: UUID,
    option_in: OptionCreate
) -> AssessmentResponse:
    """
    指定された検査に選択肢を追加します。

    - **assessment_id**: 検査のID（必須）
    - **text**: 選択肢の文言（必須）
    - **value**: スコア値（必須）
    - **order**: 表示順序（必須）
    """
    await validate_assessment_exists(assessment_id, db)
    option = Option(**option_in.model_dump())
    await assessment.add_option(db, assessment_id, option)
    return await assessment.get_with_questions(db, assessment_id)

@router.get(
    "/{assessment_id}/statistics",
    response_model=Dict[str, Any],
    summary="検査の統計情報取得"
)
async def get_assessment_statistics(
    *,
    db: AsyncSession = Depends(get_db_session),
    assessment_id: UUID
) -> Dict[str, Any]:
    """
    指定された検査の統計情報を取得します。

    - **assessment_id**: 検査のID（必須）
    """
    await validate_assessment_exists(assessment_id, db)
    stats = await assessment.get_statistics(db, assessment_id)
    completion_rate = await assessment.get_completion_rate(db, assessment_id)
    return {
        **stats,
        "completion_rate": completion_rate
    }