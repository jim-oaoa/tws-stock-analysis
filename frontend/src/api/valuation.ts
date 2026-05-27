import axios from 'axios';
import type { ValuationApiResponse, HybridSignalResult } from '../types/valuation';

// Use relative path so Vite proxy handles forwarding to backend.
// This avoids the Windows-browser → WSL localhost cross-environment dead-end.
const api = axios.create({
  baseURL: '',
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
