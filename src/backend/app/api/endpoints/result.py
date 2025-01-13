from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.api.deps import (
    get_db_session,
    get_pagination_params,
    validate_result_exists,
    validate_assessment_exists,
    validate_patient_exists
)
from app.crud.result import assessment_result
from app.schemas.result import (
    AssessmentResultCreate,
    AssessmentResultUpdate,
    AssessmentResultResponse,
    AnswerDetailCreate,
    DetailedAssessmentResult,
    AssessmentGraphData
)
from app.models.base import AssessmentStatus

router = APIRouter()

@router.post(
    "/",
    response_model=AssessmentResultResponse,
    status_code=status.HTTP_201_CREATED,
    summary="検査結果の新規作成"
)
async def create_assessment_result(
    *,
    db: AsyncSession = Depends(get_db_session),
    result_in: AssessmentResultCreate
) -> AssessmentResultResponse:
    """
    新しい検査結果を作成します。

    - **patient_id**: 患者のID（必須）
    - **assessment_id**: 検査のID（必須）
    """
    await validate_patient_exists(result_in.patient_id, db)
    await validate_assessment_exists(result_in.assessment_id, db)
    return await assessment_result.create(db, obj_in=result_in)

@router.get(
    "/{result_id}",
    response_model=DetailedAssessmentResult,
    summary="検査結果の詳細取得"
)
async def get_assessment_result(
    *,
    db: AsyncSession = Depends(get_db_session),
    result_id: UUID
) -> DetailedAssessmentResult:
    """
    指定されたIDの検査結果詳細を取得します。

    - **result_id**: 検査結果のID（必須）
    """
    await validate_result_exists(result_id, db)
    result = await assessment_result.get_with_details(db, result_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された検査結果が見つかりません"
        )
    
    # 重症度レベルの判定
    severity = await assessment_result.get_severity_level(db, result_id)
    
    return DetailedAssessmentResult(
        **result.model_dump(),
        severity_level=severity,
        is_above_cutoff=result.total_score > result.assessment.cutoff if result.total_score else False,
        completion_time=(
            (result.completed_at - result.started_at).total_seconds() / 60
            if result.completed_at and result.started_at else None
        )
    )

@router.post(
    "/{result_id}/start",
    response_model=AssessmentResultResponse,
    summary="検査の開始"
)
async def start_assessment(
    *,
    db: AsyncSession = Depends(get_db_session),
    result_id: UUID
) -> AssessmentResultResponse:
    """
    検査を開始状態にします。

    - **result_id**: 検査結果のID（必須）
    """
    await validate_result_exists(result_id, db)
    result = await assessment_result.start_assessment(db, result_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された検査結果が見つかりません"
        )
    return result

@router.post(
    "/{result_id}/complete",
    response_model=AssessmentResultResponse,
    summary="検査の完了"
)
async def complete_assessment(
    *,
    db: AsyncSession = Depends(get_db_session),
    result_id: UUID
) -> AssessmentResultResponse:
    """
    検査を完了状態にします。

    - **result_id**: 検査結果のID（必須）
    """
    await validate_result_exists(result_id, db)
    result = await assessment_result.complete_assessment(db, result_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された検査結果が見つかりません"
        )
    return result

@router.post(
    "/{result_id}/answers",
    response_model=AssessmentResultResponse,
    summary="回答の追加"
)
async def add_answer(
    *,
    db: AsyncSession = Depends(get_db_session),
    result_id: UUID,
    answer_in: AnswerDetailCreate
) -> AssessmentResultResponse:
    """
    検査結果に回答を追加します。

    - **result_id**: 検査結果のID（必須）
    - **question_id**: 質問のID（必須）
    - **selected_option_id**: 選択された選択肢のID（必須）
    - **value**: 回答の値（必須）
    """
    await validate_result_exists(result_id, db)
    result = await assessment_result.get(db, result_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された検査結果が見つかりません"
        )
    
    if result.status != AssessmentStatus.IN_PROGRESS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="進行中の検査でのみ回答を追加できます"
        )
    
    await assessment_result.add_answer(db, result_id, answer_in)
    return await assessment_result.get_with_details(db, result_id)

@router.get(
    "/{result_id}/trend",
    response_model=AssessmentGraphData,
    summary="トレンドデータの取得"
)
async def get_trend_data(
    *,
    db: AsyncSession = Depends(get_db_session),
    result_id: UUID,
    days: int = 30
) -> AssessmentGraphData:
    """
    検査結果のトレンドデータを取得します。

    - **result_id**: 検査結果のID（必須）
    - **days**: 取得する日数（デフォルト: 30日）
    """
    await validate_result_exists(result_id, db)
    result = await assessment_result.get_with_details(db, result_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された検査結果が見つかりません"
        )
    
    trend_data = await assessment_result.get_trend_data(
        db,
        result.patient_id,
        result.assessment.type,
        days=days
    )
    
    return AssessmentGraphData(
        assessment_type=result.assessment.type,
        data_points=trend_data,
        trend_line=[],  # トレンドライン計算は別途実装
        cutoff_line=result.assessment.cutoff,
        average_line=sum(d["score"] for d in trend_data) / len(trend_data) if trend_data else 0
    )