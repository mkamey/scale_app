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

# Patient スキーマ
class PatientBase(BaseModel):
    """患者の基本情報スキーマ"""
    name: str = Field(..., min_length=1, max_length=100)

class PatientCreate(PatientBase, BaseCreateSchema):
    """患者作成用スキーマ"""
    pass

class PatientUpdate(PatientBase, BaseUpdateSchema):
    """患者更新用スキーマ"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)

class PatientResponse(PatientBase, BaseResponseSchema, TimestampSchema):
    """患者レスポース用スキーマ"""
    pass

# Assessment スキーマ
class AssessmentBase(BaseModel):
    """検査の基本情報スキーマ"""
    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    cutoff: int = Field(..., ge=0)
    max_score: int = Field(..., ge=0)

class AssessmentCreate(AssessmentBase, BaseCreateSchema):
    """検査作成用スキーマ"""
    questions: List["QuestionCreate"]
    options: List["OptionCreate"]

class AssessmentUpdate(BaseUpdateSchema):
    """検査更新用スキーマ"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    type: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    cutoff: Optional[int] = Field(None, ge=0)
    max_score: Optional[int] = Field(None, ge=0)

class AssessmentResponse(AssessmentBase, BaseResponseSchema, TimestampSchema):
    """検査レスポンス用スキーマ"""
    questions: List["QuestionResponse"]
    options: List["OptionResponse"]

# Question スキーマ
class QuestionBase(BaseModel):
    """質問の基本情報スキーマ"""
    text: str = Field(..., min_length=1)
    order: int = Field(..., ge=0)

class QuestionCreate(QuestionBase, BaseCreateSchema):
    """質問作成用スキーマ"""
    pass

class QuestionUpdate(BaseUpdateSchema):
    """質問更新用スキーマ"""
    text: Optional[str] = Field(None, min_length=1)
    order: Optional[int] = Field(None, ge=0)

class QuestionResponse(QuestionBase, BaseResponseSchema):
    """質問レスポンス用スキーマ"""
    assessment_id: UUID

# Option スキーマ
class OptionBase(BaseModel):
    """選択肢の基本情報スキーマ"""
    text: str = Field(..., min_length=1)
    value: int = Field(...)
    order: int = Field(..., ge=0)

class OptionCreate(OptionBase, BaseCreateSchema):
    """選択肢作成用スキーマ"""
    pass

class OptionUpdate(BaseUpdateSchema):
    """選択肢更新用スキーマ"""
    text: Optional[str] = Field(None, min_length=1)
    value: Optional[int] = None
    order: Optional[int] = Field(None, ge=0)

class OptionResponse(OptionBase, BaseResponseSchema):
    """選択肢レスポンス用スキーマ"""
    assessment_id: UUID

# 循環参照を解決するための更新
AssessmentCreate.model_rebuild()
AssessmentResponse.model_rebuild()