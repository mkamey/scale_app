from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID

class TimestampSchema(BaseModel):
    """タイムスタンプを含むベーススキーマ"""
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class BaseResponseSchema(BaseModel):
    """レスポンス用ベーススキーマ"""
    id: UUID
    
    model_config = ConfigDict(from_attributes=True)

class BaseCreateSchema(BaseModel):
    """作成用ベーススキーマ"""
    model_config = ConfigDict(from_attributes=True)

class BaseUpdateSchema(BaseModel):
    """更新用ベーススキーマ"""
    model_config = ConfigDict(from_attributes=True)

class PaginatedResponse(BaseModel):
    """ページネーション用レスポンススキーマ"""
    total: int
    page: int
    per_page: int
    items: list
    has_next: bool
    has_prev: bool

class ErrorResponse(BaseModel):
    """エラーレスポンススキーマ"""
    message: str
    detail: Optional[str] = None
    code: Optional[str] = None