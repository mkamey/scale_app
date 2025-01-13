/**
 * ページネーション用のレスポンス型
 */
export interface PaginatedResponse<T> {
  total: number;
  page: number;
  per_page: number;
  items: T[];
  has_next: boolean;
  has_prev: boolean;
}

/**
 * 検査の型定義
 */
export interface Assessment {
  id: string;
  name: string;
  type: string;
  description?: string;
  cutoff: number;
  max_score: number;
  created_at: string;
  updated_at: string;
  questions?: Question[];
  options?: Option[];
}

/**
 * 質問の型定義
 */
export interface Question {
  id: string;
  text: string;
  order: number;
  assessment_id: string;
  created_at: string;
  updated_at: string;
}

/**
 * 選択肢の型定義
 */
export interface Option {
  id: string;
  text: string;
  value: number;
  order: number;
  assessment_id: string;
  created_at: string;
  updated_at: string;
}

/**
 * 検査作成用の型定義
 */
export interface AssessmentCreate {
  name: string;
  type: string;
  description?: string;
  cutoff: number;
  max_score: number;
  questions?: {
    text: string;
    order: number;
  }[];
  options?: {
    text: string;
    value: number;
    order: number;
  }[];
}

/**
 * 検査更新用の型定義
 */
export interface AssessmentUpdate {
  name?: string;
  type?: string;
  description?: string;
  cutoff?: number;
  max_score?: number;
}

/**
 * 検査の統計情報の型定義
 */
export interface AssessmentStatistics {
  total_assessments: number;
  average_score: number;
  completion_rate: number;
  above_cutoff_count: number;
  below_cutoff_count: number;
}

/**
 * APIのエラーレスポンスの型定義
 */
export interface ApiError {
  message: string;
  detail?: string;
}