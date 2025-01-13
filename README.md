<div align="center">
  <img src="assets/header.svg" alt="Scale App - Psychological Assessment Management System" width="800">
</div>

# 🎯 Scale App - 心理検査管理システム

## 📋 概要

Scale Appは、精神科外来での心理検査を効率的に管理するためのシステムです。iPadを使用して患者が心理検査を入力し、医師がリアルタイムで結果を確認できる統合プラットフォームを提供します。

## ✨ 主な機能

### 👤 患者向け機能
- 割り当てられた心理検査の一覧表示
- 各検査の状態管理（未回答/回答中/完了）
- タッチ操作に最適化された回答インターフェース
- 進捗状況のリアルタイム表示
- 回答データの自動保存機能

### 👨‍⚕️ 医師向け機能
- ドーナツグラフによる視覚的な結果表示
- カットオフ値超過の警告システム
- 12種類の検査結果の一括表示
- 重症度評価の可視化
- 検査実施履歴の管理

## 📊 対応心理検査
- 作成中
## 🛠 技術スタック

### フロントエンド
- Remix (React)
- Tailwind CSS
- shadcn/ui コンポーネント

### バックエンド
- FastAPI (Python)
- SQLAlchemy (ORM)

### データベース
- SQLite / PostgreSQL

### インフラ
- Docker
- Docker Compose

## 🔒 セキュリティ機能
- 医師用アカウント管理システム
- 患者データアクセス制御
- データベースの自動バックアップ
- 患者情報の暗号化

## 🚀 開発環境のセットアップ

```bash
# リポジトリのクローン
git clone [repository-url]
cd scale-app

# 開発環境の起動
docker-compose up -d
```

## 📝 ライセンス
このプロジェクトは [MIT License](LICENSE) の下で公開されています。

## 👥 コントリビューション
プロジェクトへの貢献は大歓迎です。Issue や Pull Request を通じて、プロジェクトの改善にご協力ください。