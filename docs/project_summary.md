# 心理検査管理システム プロジェクト概要

## 1. バックエンドAPI実装

### 技術スタック
- FastAPI (Python)
- SQLAlchemy (ORM)
- SQLite/PostgreSQL

### 主要エンドポイント
- 患者管理API
- 検査マスターAPI
- 検査結果API

### 特徴
- 型安全なAPI設計
- OpenAPIドキュメント自動生成
- CORS設定
- グローバルエラーハンドリング

## 2. データモデル設計

### 主要テーブル
- Patients（患者）
- Assessments（検査マスター）
- Questions（質問）
- Options（選択肢）
- AssessmentResults（検査結果）
- AnswerDetails（回答詳細）

### リレーションシップ
- 1対多: 患者 ↔ 検査結果
- 1対多: 検査マスター ↔ 質問
- 1対多: 質問 ↔ 選択肢

## 3. セキュリティ要件

### 実装内容
- 認証・認可システム
- 患者データアクセス制御
- データ暗号化
- バックアップ機構

## 4. フロントエンド初期設定

### 技術スタック
- Remix (React)
- Tailwind CSS
- shadcn/ui

### 設定済み項目
- Tailwind CSS設定
- 基本プロジェクト構成
- ルーティング設定

## 5. インフラ構成

### 環境
- Docker
- Docker Compose
- オンプレミス環境

### 特徴
- コンテナ化による環境の一貫性
- 小規模運用向け最適化
- クローズドネットワーク対応

## 再構築手順

1. バックエンドAPIのセットアップ
```bash
cd src/backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

2. フロントエンドのセットアップ
```bash
cd src/frontend
npm install
npm run dev
```

3. Docker環境の構築
```bash
docker-compose up -d
```

## コミット履歴
- 🚀 feat: バックエンドAPIの実装完了
- 🛠️ refactor: データモデルの最適化
- 🔒 chore: セキュリティ設定の追加
- 🎨 style: フロントエンド初期設定