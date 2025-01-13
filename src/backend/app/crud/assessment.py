from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.models import Assessment, Question, Option, AssessmentResult
from app.schemas.assessment import AssessmentCreate, AssessmentUpdate

class CRUDAssessment(CRUDBase[Assessment, AssessmentCreate, AssessmentUpdate]):
    """
    検査モデルに対するCRUD操作
    """
    async def get_with_questions(
        self,
        db: AsyncSession,
        assessment_id: UUID
    ) -> Optional[Assessment]:
        """
        質問を含む検査情報の取得
        """
        query = (
            select(Assessment)
            .options(
                joinedload(Assessment.questions),
                joinedload(Assessment.options)
            )
            .where(Assessment.id == assessment_id)
        )
        result = await db.execute(query)
        return result.unique().scalar_one_or_none()

    async def get_by_type(
        self,
        db: AsyncSession,
        assessment_type: str
    ) -> List[Assessment]:
        """
        タイプによる検査の取得
        """
        query = select(Assessment).where(Assessment.type == assessment_type)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_statistics(
        self,
        db: AsyncSession,
        assessment_id: UUID
    ) -> Dict[str, Any]:
        """
        検査結果の統計情報の取得
        """
        query = (
            select(
                func.count(AssessmentResult.id).label("total_attempts"),
                func.avg(AssessmentResult.total_score).label("average_score"),
                func.min(AssessmentResult.total_score).label("min_score"),
                func.max(AssessmentResult.total_score).label("max_score")
            )
            .where(
                AssessmentResult.assessment_id == assessment_id,
                AssessmentResult.status == "completed"
            )
        )
        result = await db.execute(query)
        stats = result.one()
        
        return {
            "total_attempts": stats.total_attempts,
            "average_score": float(stats.average_score) if stats.average_score else 0.0,
            "min_score": stats.min_score,
            "max_score": stats.max_score
        }

    async def add_question(
        self,
        db: AsyncSession,
        assessment_id: UUID,
        question: Question
    ) -> Question:
        """
        質問の追加
        """
        question.assessment_id = assessment_id
        db.add(question)
        await db.commit()
        await db.refresh(question)
        return question

    async def add_option(
        self,
        db: AsyncSession,
        assessment_id: UUID,
        option: Option
    ) -> Option:
        """
        選択肢の追加
        """
        option.assessment_id = assessment_id
        db.add(option)
        await db.commit()
        await db.refresh(option)
        return option

    async def get_completion_rate(
        self,
        db: AsyncSession,
        assessment_id: UUID
    ) -> float:
        """
        検査の完了率の取得
        """
        total_query = select(func.count(AssessmentResult.id)).where(
            AssessmentResult.assessment_id == assessment_id
        )
        completed_query = select(func.count(AssessmentResult.id)).where(
            AssessmentResult.assessment_id == assessment_id,
            AssessmentResult.status == "completed"
        )
        
        total = await db.execute(total_query)
        completed = await db.execute(completed_query)
        
        total_count = total.scalar()
        completed_count = completed.scalar()
        
        return (completed_count / total_count * 100) if total_count > 0 else 0.0

# CRUDAssessmentのインスタンスを作成
assessment = CRUDAssessment(Assessment)