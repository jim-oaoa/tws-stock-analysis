export enum ValuationZone {
  FISH_HEAD = 'FISH_HEAD',
  FISH_BODY = 'FISH_BODY',
  FISH_TAIL_LOW = 'FISH_TAIL_LOW',
  FISH_TAIL_HIGH = 'FISH_TAIL_HIGH',
  FISH_BONE = 'FISH_BONE',
}

export enum FundamentalZone {
  UNDERVALUED = 'UNDERVALUED',
  FAIR = 'FAIR',
  OVERVALUED = 'OVERVALUED',
  BUBBLE = 'BUBBLE',
}

export enum TechnicalState {
  BULLISH = 'BULLISH',
  NEUTRAL = 'NEUTRAL',
  BEARISH = 'BEARISH',
  OVEREXTENDED = 'OVEREXTENDED',
}

export enum HybridSignal {
  STRONG_BUY = 'STRONG_BUY',
  BUY = 'BUY',
  HOLD = 'HOLD',
  SELL = 'SELL',
  STRONG_SELL = 'STRONG_SELL',
}

export interface ValuationZoneLevels {
  fish_head: number;
  fish_body: number;
  fish_tail_low: number;
  fish_tail_high: number;
  fish_bone: number;
}

export interface ValuationResult {
  symbol: string;
  price: number;
  net_value: number;
  zones: ValuationZoneLevels;
  current_zone: ValuationZone;
}

export interface TechnicalStateResult {
  state: TechnicalState;
  fish_bone_value: number;
  bias: number;
  adx: number;
}

export interface QuarterlyGridCell {
  year: number;
  quarter: number;
  eps: number;
  oci: number;
  other_items: number;
  dividends: number;
  adjustment_amount: number;
  accumulated_net_value: number;
}

export interface ValuationApiResponse {
  valuation: ValuationResult;
  quarterly_grid: QuarterlyGridCell[];
  fundamental_zone: FundamentalZone;
}

export interface HybridSignalResult {
  symbol: string;
  fundamental_zone: FundamentalZone;
  technical_state: TechnicalState;
  final_signal: HybridSignal;
  action: string;
  valuation: ValuationResult;
  technical: TechnicalStateResult;
}
