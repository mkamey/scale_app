from fastapi import APIRouter
from app.api.endpoints import patient, assessment, result

# APIルーターの作成
api_router = APIRouter()

# 各エンドポイントのルーターを登録
api_router.include_router(
    patient.router,
    prefix="/patients",
    tags=["patients"]
)

api_router.include_router(
    assessment.router,
    prefix="/assessments",
    tags=["assessments"]
)

api_router.include_router(
    result.router,
    prefix="/results",
    tags=["results"]
)