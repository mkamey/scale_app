import { ApiError } from "../types/api";

const API_BASE_URL = "http://localhost:8000/api/v1"; // バックエンドのAPIベースURL

/**
 * APIクライアントの共通関数
 * @param url APIのURL
 * @param method HTTPメソッド
 * @param data リクエストボディ
 * @returns レスポンスデータ
 */
export async function apiClient<T>(
  url: string,
  method: "GET" | "POST" | "PUT" | "DELETE",
  data?: any
): Promise<T> {
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };

  const options: RequestInit = {
    method,
    headers,
    body: data ? JSON.stringify(data) : undefined,
  };

  try {
    const response = await fetch(API_BASE_URL + url, options);

    if (!response.ok) {
      let error: ApiError;
      try {
        error = await response.json();
      } catch (e) {
        error = { message: response.statusText };
      }
      throw new Error(JSON.stringify(error));
    }

    if (response.status === 204) {
      return {} as T;
    }

    return await response.json();
  } catch (e: any) {
    let error: ApiError;
    try {
      error = JSON.parse(e.message);
    } catch (parseError) {
      error = { message: e.message };
    }
    throw error;
  }
}