import React from 'react';
import type { ValuationResult, FundamentalZone } from '../types/valuation';

interface PriceHeroProps {
  valuation: ValuationResult;
  fundamentalZone: FundamentalZone;
}

const zoneColorMap: Record<string, { bg: string; text: string; label: string }> = {
  UNDERVALUED: { bg: 'var(--profit-dim)', text: 'var(--profit)', label: '低估' },
  FAIR: { bg: 'var(--warning-dim)', text: 'var(--warning)', label: '合理價' },
  OVERVALUED: { bg: 'var(--loss-dim)', text: 'var(--loss)', label: '高估' },
  BUBBLE: { bg: 'var(--loss-dim)', text: 'var(--loss)', label: '泡沫' },
};

const valuationZoneLabel: Record<string, string> = {
  FISH_HEAD: '🐟 魚頭區',
  FISH_BODY: '🐟 魚身區',
  FISH_TAIL_LOW: '🐟 魚尾低區',
  FISH_TAIL_HIGH: '🐟 魚尾高區',
  FISH_BONE: '🦴 魚骨區',
  BONE_BROKEN: '💀 斷骨區',
};

function formatNetValue(value: number): string {
  if (value >= 1e12) return `NT$ ${(value / 1e12).toFixed(2)} 兆`;
  if (value >= 1e8) return `NT$ ${(value / 1e8).toFixed(2)} 億`;
  return `NT$ ${value.toLocaleString(undefined, { maximumFractionDigits: 0 })}`;
}

export const PriceHero: React.FC<PriceHeroProps> = ({ valuation, fundamentalZone }) => {
  const zoneInfo = zoneColorMap[fundamentalZone] || zoneColorMap.FAIR;
  const valZoneLabel = valuationZoneLabel[valuation.current_zone] || valuation.current_zone;

  return (
    <div
      className="relative overflow-hidden rounded-[var(--radius-xl)] border border-[var(--border-default)] p-6 md:p-8 shadow-[var(--elevation-1)] transition-all duration-[var(--duration-normal)] ease-[var(--easing)] hover:-translate-y-0.5 hover:shadow-[var(--elevation-2)]"
      style={{
        background: 'linear-gradient(135deg, var(--bg-surface) 0%, transparent 100%)',
      }}
    >
      {/* Zone badge */}
      <div className="flex flex-wrap items-center gap-3 mb-4">
        <span
          className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold"
          style={{ backgroundColor: zoneInfo.bg, color: zoneInfo.text }}
        >
          {zoneInfo.label}
        </span>
        <span className="text-xs text-[var(--text-secondary)]">
          {valZoneLabel}
        </span>
      </div>

      {/* Massive price */}
      <div className="mb-3">
        <span className="text-sm text-[var(--text-secondary)] font-medium mr-2">NT$</span>
        <span className="text-4xl md:text-5xl font-black text-[var(--text-primary)] tabular-nums">
          {valuation.price?.toLocaleString(undefined, { maximumFractionDigits: 0 }) ?? '—'}
        </span>
      </div>

      {/* Net value subtitle */}
      <div className="text-sm text-[var(--text-secondary)]">
        淨值： <span className="text-[var(--text-primary)] font-semibold tabular-nums font-mono">
          {valuation.net_value != null ? formatNetValue(valuation.net_value) : '—'}
        </span>
      </div>
    </div>
  );
};
