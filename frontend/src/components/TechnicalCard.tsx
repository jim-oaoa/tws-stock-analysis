import React from 'react';
import type { TechnicalStateResult } from '../types/valuation';

interface TechnicalCardProps {
  technical: TechnicalStateResult;
}

const stateColorMap: Record<string, string> = {
  BULLISH: 'var(--profit)',
  NEUTRAL: 'var(--warning)',
  BEARISH: 'var(--loss)',
  OVEREXTENDED: 'var(--loss)',
};

const stateLabelMap: Record<string, string> = {
  BULLISH: '多頭',
  NEUTRAL: '中性',
  BEARISH: '空頭',
  OVEREXTENDED: '過熱',
};

function getBiasColor(bias: number): { color: string; barColor: string } {
  const absBias = Math.abs(bias);
  if (absBias <= 10) return { color: 'var(--profit)', barColor: 'var(--profit)' };
  if (absBias <= 20) return { color: 'var(--warning)', barColor: 'var(--warning)' };
  return { color: 'var(--loss)', barColor: 'var(--loss)' };
}

export const TechnicalCard: React.FC<TechnicalCardProps> = ({ technical }) => {
  const stateColor = stateColorMap[technical.state] || 'var(--text-secondary)';
  const stateDisplay = stateLabelMap[technical.state] || technical.state?.replace('_', ' ') || '無';
  const biasInfo = getBiasColor(technical.bias);
  const adxTrending = technical.adx > 25;

  // Normalize bias absolute value to a percentage for the progress bar (cap at 50%)
  const biasBarWidth = Math.min(Math.abs(technical.bias), 50) * 2; // 0-100%

  return (
    <div className="bg-[var(--bg-surface)] rounded-[var(--radius-lg)] p-5 shadow-[var(--elevation-1)] transition-all duration-[var(--duration-normal)] ease-[var(--easing)] hover:shadow-[var(--elevation-2)] space-y-4">
      <h3 className="text-xs font-semibold text-[var(--text-secondary)] uppercase tracking-wider">
        技術指標
      </h3>

      {/* Fish Bone Value */}
      <div className="space-y-1">
        <div className="text-xs text-[var(--text-secondary)]">魚骨價值</div>
        <div className="text-lg font-semibold text-[var(--text-primary)] tabular-nums font-mono">
          NT$ {technical.fish_bone_value?.toLocaleString(undefined, { maximumFractionDigits: 0 }) ?? '—'}
        </div>
      </div>

      {/* BIAS with progress bar */}
      <div className="space-y-1.5">
        <div className="flex justify-between items-center">
          <span className="text-xs text-[var(--text-secondary)]">乖離率</span>
          <span
            className="text-sm font-semibold tabular-nums"
            style={{ color: biasInfo.color }}
          >
            {technical.bias > 0 ? '+' : ''}{technical.bias?.toFixed(2) ?? '—'}%
          </span>
        </div>
        <div className="h-2 bg-[var(--bg-elevated)] rounded-full overflow-hidden">
          <div
            className="h-full rounded-full transition-all duration-[var(--duration-slow)] ease-[var(--easing)]"
            style={{
              width: `${biasBarWidth}%`,
              backgroundColor: biasInfo.barColor,
            }}
          />
        </div>
      </div>

      {/* ADX with traffic light */}
      <div className="flex items-center justify-between">
        <span className="text-xs text-[var(--text-secondary)]">趨向指標</span>
        <div className="flex items-center gap-2">
          <span className="text-sm font-semibold tabular-nums text-[var(--text-primary)]">
            {technical.adx?.toFixed(1) ?? '—'}
          </span>
          <span
            className="inline-block w-2.5 h-2.5 rounded-full"
            style={{ backgroundColor: adxTrending ? 'var(--profit)' : 'var(--text-secondary)' }}
            aria-label={adxTrending ? '趨勢明確' : '盤整中'}
          />
          <span
            className="text-xs font-medium"
            style={{ color: adxTrending ? 'var(--profit)' : 'var(--text-secondary)' }}
          >
            {adxTrending ? '趨勢明確' : '盤整中'}
          </span>
        </div>
      </div>

      {/* Technical State */}
      <div className="pt-3 border-t" style={{ borderColor: 'var(--divider)' }}>
        <div className="flex items-center justify-between">
          <span className="text-xs text-[var(--text-secondary)]">技術狀態</span>
          <span
            className="text-sm font-semibold"
            style={{ color: stateColor }}
          >
            {stateDisplay}
          </span>
        </div>
      </div>
    </div>
  );
};
