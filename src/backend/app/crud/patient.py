from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.models import Patient, AssessmentResult
from app.schemas.assessment import PatientCreate, PatientUpdate

class CRUDPatient(CRUDBase[Patient, PatientCreate, PatientUpdate]):
    """
    患者モデルに対するCRUD操作
    """
    async def get_with_results(
        self,
        db: AsyncSession,
        patient_id: UUID
    ) -> Optional[Patient]:
        """
        検査結果を含む患者情報の取得
        """
        query = (
            select(Patient)
            .options(joinedload(Patient.assessment_results))
            .where(Patient.id == patient_id)
        )
        result = await db.execute(query)
        return result.unique().scalar_one_or_none()

    async def get_active_assessments(
        self,
        db: AsyncSession,
        patient_id: UUID
    ) -> List[AssessmentResult]:
        """
        進行中の検査の取得
        """
        query = (
            select(AssessmentResult)
            .join(Patient)
            .where(
                Patient.id == patient_id,
                AssessmentResult.status != "completed"
            )
            .order_by(AssessmentResult.created_at.desc())
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def get_completed_assessments(
        self,
        db: AsyncSession,
        patient_id: UUID,
        *,
        skip: int = 0,
        limit: int = 10
    ) -> List[AssessmentResult]:
        """
        完了した検査の取得（ページネーション対応）
        """
        query = (
            select(AssessmentResult)
            .join(Patient)
            .where(
                Patient.id == patient_id,
                AssessmentResult.status == "completed"
            )
            .order_by(AssessmentResult.completed_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def get_assessment_history(
        self,
        db: AsyncSession,
        patient_id: UUID,
        assessment_type: str
    ) -> List[AssessmentResult]:
        """
        特定の種類の検査履歴の取得
        """
        query = (
            select(AssessmentResult)
            .join(Patient)
            .where(
                Patient.id == patient_id,
                AssessmentResult.status == "completed"
            )
            .order_by(AssessmentResult.completed_at.desc())
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def search_by_name(
        self,
        db: AsyncSession,
        name: str,
        *,
        skip: int = 0,
        limit: int = 10
    ) -> List[Patient]:
        """
        名前による患者検索
        """
        query = (
            select(Patient)
            .where(Patient.name.ilike(f"%{name}%"))
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

# CRUDPatientのインスタンスを作成
patient = CRUDPatient(Patient)