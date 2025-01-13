import { apiClient } from "../utils/apiClient";
import {
  Assessment,
  AssessmentCreate,
  AssessmentUpdate,
  PaginatedResponse,
  AssessmentStatistics,
} from "../types/api";

const ASSESSMENT_BASE_URL = "/assessments";

/**
 * 検査関連のAPIフック
 */
export function useAssessments() {
  /**
   * 検査一覧を取得する
   * @param skip スキップする件数
   * @param limit 取得する最大件数
   * @returns 検査一覧
   */
  const getAssessments = async (
    skip: number = 0,
    limit: number = 10
  ): Promise<PaginatedResponse<Assessment>> => {
    return await apiClient<PaginatedResponse<Assessment>>(
      `${ASSESSMENT_BASE_URL}?skip=${skip}&limit=${limit}`,
      "GET"
    );
  };

  /**
   * 検査をIDで取得する
   * @param assessmentId 検査ID
   * @returns 検査情報
   */
  const getAssessment = async (
    assessmentId: string
  ): Promise<Assessment> => {
    return await apiClient<Assessment>(
      `${ASSESSMENT_BASE_URL}/${assessmentId}`,
      "GET"
    );
  };

  /**
   * 検査を作成する
   * @param assessment 検査作成情報
   * @returns 作成された検査情報
   */
  const createAssessment = async (
    assessment: AssessmentCreate
  ): Promise<Assessment> => {
    return await apiClient<Assessment>(ASSESSMENT_BASE_URL, "POST", assessment);
  };

  /**
   * 検査を更新する
   * @param assessmentId 検査ID
   * @param assessment 検査更新情報
   * @returns 更新された検査情報
   */
  const updateAssessment = async (
    assessmentId: string,
    assessment: AssessmentUpdate
  ): Promise<Assessment> => {
    return await apiClient<Assessment>(
      `${ASSESSMENT_BASE_URL}/${assessmentId}`,
      "PUT",
      assessment
    );
  };

  /**
   * 検査を削除する
   * @param assessmentId 検査ID
   */
  const deleteAssessment = async (assessmentId: string): Promise<void> => {
    return await apiClient<void>(
      `${ASSESSMENT_BASE_URL}/${assessmentId}`,
      "DELETE"
    );
  };

  /**
   * 検査の統計情報を取得する
   * @param assessmentId 検査ID
   * @returns 検査の統計情報
   */
  const getAssessmentStatistics = async (
    assessmentId: string
  ): Promise<AssessmentStatistics> => {
    return await apiClient<AssessmentStatistics>(
      `${ASSESSMENT_BASE_URL}/${assessmentId}/statistics`,
      "GET"
    );
  };

  return {
    getAssessments,
    getAssessment,
    createAssessment,
    updateAssessment,
    deleteAssessment,
    getAssessmentStatistics,
  };
}