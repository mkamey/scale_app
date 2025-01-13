from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from app.models.base import AssessmentStatus
from app.schemas.base import (
    BaseResponseSchema,
    BaseCreateSchema,
    BaseUpdateSchema,
    TimestampSchema
)

# AssessmentResult スキーマ
class AssessmentResultBase(BaseModel):
    """検査結果の基本情報スキーマ"""
    patient_id: UUID
    assessment_id: UUID
    status: AssessmentStatus = Field(default=AssessmentStatus.NOT_STARTED)
    total_score: Optional[int] = None

class AssessmentResultCreate(AssessmentResultBase, BaseCreateSchema):
    """検査結果作成用スキーマ"""
    pass

class AssessmentResultUpdate(BaseUpdateSchema):
    """検査結果更新用スキーマ"""
    status: Optional[AssessmentStatus] = None
    total_score: Optional[int] = None

class AssessmentResultResponse(AssessmentResultBase, BaseResponseSchema, TimestampSchema):
    """検査結果レスポンス用スキーマ"""
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    answer_details: List["AnswerDetailResponse"] = []

# AnswerDetail スキーマ
class AnswerDetailBase(BaseModel):
    """回答詳細の基本情報スキーマ"""
    question_id: UUID
    selected_option_id: UUID
    value: int = Field(..., ge=0)

class AnswerDetailCreate(AnswerDetailBase, BaseCreateSchema):
    """回答詳細作成用スキーマ"""
    result_id: UUID

class AnswerDetailUpdate(BaseUpdateSchema):
    """回答詳細更新用スキーマ"""
    selected_option_id: Optional[UUID] = None
    value: Optional[int] = Field(None, ge=0)

class AnswerDetailResponse(AnswerDetailBase, BaseResponseSchema, TimestampSchema):
    """回答詳細レスポンス用スキーマ"""
    result_id: UUID
    answered_at: datetime

# 集計用スキーマ
class AssessmentSummary(BaseModel):
    """検査結果サマリースキーマ"""
    total_assessments: int
    completed_assessments: int
    average_score: float
    completion_rate: float
    assessment_type: str
    last_assessment_date: Optional[datetime]

class PatientAssessmentSummary(BaseModel):
    """患者の検査結果サマリースキーマ"""
    patient_id: UUID
    patient_name: str
    assessments: List[AssessmentSummary]
    total_completed: int
    last_assessment_date: Optional[datetime]

# 検査結果の詳細表示用スキーマ
class DetailedAssessmentResult(AssessmentResultResponse):
    """詳細な検査結果表示用スキーマ"""
    patient_name: str
    assessment_name: str
    assessment_type: str
    cutoff_value: int
    severity_level: str = Field(...)  # 重症度レベル
    is_above_cutoff: bool
    completion_time: Optional[float] = None  # 完了までの時間（分）
    trend_data: Optional[List[float]] = None  # 経時的なスコアデータ

# グラフ表示用スキーマ
class GraphDataPoint(BaseModel):
    """グラフデータポイントスキーマ"""
    date: datetime
    value: float
    label: Optional[str] = None

class AssessmentGraphData(BaseModel):
    """検査グラフデータスキーマ"""
    assessment_type: str
    data_points: List[GraphDataPoint]
    trend_line: List[float]
    cutoff_line: float
    average_line: float

# 循環参照を解決するための更新
AssessmentResultResponse.model_rebuild()