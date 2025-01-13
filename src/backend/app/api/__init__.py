from fastapi import APIRouter
from app.api.endpoints import patient, assessment, result

# APIルーターの作成
api_router = APIRouter()

# ルートエンドポイントの追加
@api_router.get("/")
async def read_root():
    return {"message": "Welcome to the Scale App API"}

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