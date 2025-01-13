from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, timedelta
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.models import AssessmentResult, AnswerDetail, Assessment
from app.models.base import AssessmentStatus
from app.schemas.result import AssessmentResultCreate, AssessmentResultUpdate

class CRUDAssessmentResult(CRUDBase[AssessmentResult, AssessmentResultCreate, AssessmentResultUpdate]):
    """
    検査結果モデルに対するCRUD操作
    """
    async def get_with_details(
        self,
        db: AsyncSession,
        result_id: UUID
    ) -> Optional[AssessmentResult]:
        """
        回答詳細を含む検査結果の取得
        """
        query = (
            select(AssessmentResult)
            .options(
                joinedload(AssessmentResult.answer_details)
                .joinedload(AnswerDetail.question),
                joinedload(AssessmentResult.assessment)
            )
            .where(AssessmentResult.id == result_id)
        )
        result = await db.execute(query)
        return result.unique().scalar_one_or_none()

    async def add_answer(
        self,
        db: AsyncSession,
        result_id: UUID,
        answer: AnswerDetail
    ) -> AnswerDetail:
        """
        回答の追加
        """
        answer.result_id = result_id
        answer.answered_at = datetime.now()
        db.add(answer)
        await db.commit()
        await db.refresh(answer)
        return answer

    async def start_assessment(
        self,
        db: AsyncSession,
        result_id: UUID
    ) -> AssessmentResult:
        """
        検査の開始
        """
        result = await self.get(db, result_id)
        if result and result.status == AssessmentStatus.NOT_STARTED:
            result.status = AssessmentStatus.IN_PROGRESS
            result.started_at = datetime.now()
            await db.commit()
            await db.refresh(result)
        return result

    async def complete_assessment(
        self,
        db: AsyncSession,
        result_id: UUID
    ) -> AssessmentResult:
        """
        検査の完了
        """
        result = await self.get(db, result_id)
        if result and result.status == AssessmentStatus.IN_PROGRESS:
            result.status = AssessmentStatus.COMPLETED
            result.completed_at = datetime.now()
            # 合計スコアの計算
            total = await self.calculate_total_score(db, result_id)
            result.total_score = total
            await db.commit()
            await db.refresh(result)
        return result

    async def calculate_total_score(
        self,
        db: AsyncSession,
        result_id: UUID
    ) -> int:
        """
        合計スコアの計算
        """
        query = (
            select(func.sum(AnswerDetail.value))
            .where(AnswerDetail.result_id == result_id)
        )
        result = await db.execute(query)
        return result.scalar() or 0

    async def get_trend_data(
        self,
        db: AsyncSession,
        patient_id: UUID,
        assessment_type: str,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """
        トレンドデータの取得
        """
        start_date = datetime.now() - timedelta(days=days)
        query = (
            select(
                AssessmentResult.completed_at,
                AssessmentResult.total_score,
                Assessment.type
            )
            .join(Assessment)
            .where(
                and_(
                    AssessmentResult.patient_id == patient_id,
                    Assessment.type == assessment_type,
                    AssessmentResult.status == AssessmentStatus.COMPLETED,
                    AssessmentResult.completed_at >= start_date
                )
            )
            .order_by(AssessmentResult.completed_at)
        )
        result = await db.execute(query)
        return [
            {
                "date": row.completed_at,
                "score": row.total_score,
                "type": row.type
            }
            for row in result
        ]

    async def get_severity_level(
        self,
        db: AsyncSession,
        result_id: UUID
    ) -> str:
        """
        重症度レベルの判定
        """
        result = await self.get_with_details(db, result_id)
        if not result or not result.assessment:
            return "unknown"

        score = result.total_score or 0
        cutoff = result.assessment.cutoff
        max_score = result.assessment.max_score

        if score >= cutoff:
            if score >= max_score * 0.8:
                return "severe"
            elif score >= max_score * 0.6:
                return "moderate"
            else:
                return "mild"
        return "normal"

# CRUDAssessmentResultのインスタンスを作成
assessment_result = CRUDAssessmentResult(AssessmentResult)