from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query  # Queryをインポート
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.api.deps import (
    get_db_session,
    get_pagination_params,
    validate_patient_exists
)
from app.crud.patient import patient
from app.schemas.assessment import (
    PatientCreate,
    PatientUpdate,
    PatientResponse
)
from app.schemas.result import (
    AssessmentResultResponse,
    PatientAssessmentSummary
)
from app.schemas.base import PaginatedResponse

router = APIRouter()

@router.post(
    "/",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
    summary="患者の新規作成"
)
async def create_patient(
    *,
    db: AsyncSession = Depends(get_db_session),
    patient_in: PatientCreate
) -> PatientResponse:
    """
    新しい患者を作成します。

    - **name**: 患者の氏名（必須）
    """
    return await patient.create(db, obj_in=patient_in)

@router.get(
    "/{patient_id}",
    response_model=PatientResponse,
    summary="患者情報の取得"
)
async def get_patient(
    *,
    db: AsyncSession = Depends(get_db_session),
    patient_id: UUID
) -> PatientResponse:
    """
    指定されたIDの患者情報を取得します。

    - **patient_id**: 患者のID（必須）
    """
    await validate_patient_exists(patient_id, db)
    result = await patient.get(db, patient_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された患者が見つかりません"
        )
    return result

@router.put(
    "/{patient_id}",
    response_model=PatientResponse,
    summary="患者情報の更新"
)
async def update_patient(
    *,
    db: AsyncSession = Depends(get_db_session),
    patient_id: UUID,
    patient_in: PatientUpdate
) -> PatientResponse:
    """
    指定されたIDの患者情報を更新します。

    - **patient_id**: 患者のID（必須）
    - **name**: 更新する氏名
    """
    await validate_patient_exists(patient_id, db)
    db_obj = await patient.get(db, patient_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された患者が見つかりません"
        )
    return await patient.update(db, db_obj=db_obj, obj_in=patient_in)

@router.delete(
    "/{patient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="患者の削除"
)
async def delete_patient(
    *,
    db: AsyncSession = Depends(get_db_session),
    patient_id: UUID
) -> None:
    """
    指定されたIDの患者を削除します。

    - **patient_id**: 患者のID（必須）
    """
    await validate_patient_exists(patient_id, db)
    await patient.remove(db, id=patient_id)

@router.get(
    "/",
    response_model=PaginatedResponse,
    summary="患者一覧の取得"
)
async def list_patients(
    *,
    db: AsyncSession = Depends(get_db_session),
    pagination: dict[str, int] = Depends(get_pagination_params)  # 整数として取得
) -> PaginatedResponse:
    """
    患者の一覧を取得します。

    - **skip**: スキップする件数
    - **limit**: 取得する最大件数
    """
    skip, limit = pagination["skip"], pagination["limit"]
    patients = await patient.get_multi(db, skip=skip, limit=limit)  # 引数を正しく渡す
    total = len(patients)  # 本来はcount queryを使用すべき
    return PaginatedResponse(
        total=total,
        page=skip // limit + 1,
        per_page=limit,
        items=patients,
        has_next=total == limit,
        has_prev=skip > 0
    )

@router.get(
    "/{patient_id}/assessments",
    response_model=List[AssessmentResultResponse],
    summary="患者の検査結果一覧の取得"
)
async def get_patient_assessments(
    *,
    db: AsyncSession = Depends(get_db_session),
    patient_id: UUID,
    pagination: tuple[int, int] = Depends(get_pagination_params)
) -> List[AssessmentResultResponse]:
    """
    指定された患者の検査結果一覧を取得します。

    - **patient_id**: 患者のID（必須）
    - **skip**: スキップする件数
    - **limit**: 取得する最大件数
    """
    await validate_patient_exists(patient_id, db)
    skip, limit = pagination
    return await patient.get_completed_assessments(
        db,
        patient_id,
        skip=skip,
        limit=limit
    )

@router.get(
    "/{patient_id}/summary",
    response_model=PatientAssessmentSummary,
    summary="患者の検査サマリーの取得"
)
async def get_patient_summary(
    *,
    db: AsyncSession = Depends(get_db_session),
    patient_id: UUID
) -> PatientAssessmentSummary:
    """
    指定された患者の検査サマリーを取得します。

    - **patient_id**: 患者のID（必須）
    """
    await validate_patient_exists(patient_id, db)
    db_patient = await patient.get_with_results(db, patient_id)
    if not db_patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された患者が見つかりません"
        )
    
    # サマリー情報の集計処理は実際にはより複雑になる
    return PatientAssessmentSummary(
        patient_id=db_patient.id,
        patient_name=db_patient.name,
        assessments=[],  # 実際には検査タイプごとの集計を行う
        total_completed=len([
            r for r in db_patient.assessment_results
            if r.status == "completed"
        ]),
        last_assessment_date=max(
            (r.completed_at for r in db_patient.assessment_results
             if r.completed_at),
            default=None
        )
    )