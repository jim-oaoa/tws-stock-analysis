import axios from 'axios';
import type { ValuationApiResponse, HybridSignalResult } from '../types/valuation';

const API_BASE_URL = 'http://localhost:8001';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Fetches valuation data for a given symbol.
 * @param symbol The stock symbol to fetch valuation for.
 * @param period Optional period parameter.
 * @returns A promise that resolves to the ValuationApiResponse.
 */
export const fetchValuation = async (symbol: string, period?: string): Promise<ValuationApiResponse> => {
  const response = await api.get<ValuationApiResponse>(`/valuation/${symbol}`, {
    params: { period },
  });
  return response.data;
};

/**
 * Fetches the hybrid signal for a given symbol.
 * @param symbol The stock symbol to fetch signal for.
 * @param period Optional period parameter.
 * @returns A promise that resolves to the HybridSignalResult.
 */
export const fetchSignal = async (symbol: string, period?: string): Promise<HybridSignalResult> => {
  const response = await api.get<HybridSignalResult>(`/valuation/signal/${symbol}`, {
    params: { period },
  });
  return response.data;
};

export default api;
