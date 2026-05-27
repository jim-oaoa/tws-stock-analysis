import React from 'react';
import type { ValuationResult, FundamentalZone } from '../types/valuation';

interface PriceHeroProps {
  valuation: ValuationResult;
  fundamentalZone: FundamentalZone;
}

const zoneColorMap: Record<string, { bg: string; text: string; label: string }> = {
  UNDERVALUED: { bg: 'var(--profit-dim)', text: 'var(--profit)', label: 'Undervalued' },
  FAIR: { bg: 'var(--warning-dim)', text: 'var(--warning)', label: 'Fair Value' },
  OVERVALUED: { bg: 'var(--loss-dim)', text: 'var(--loss)', label: 'Overvalued' },
  BUBBLE: { bg: 'var(--loss-dim)', text: 'var(--loss)', label: 'Bubble' },
};

const valuationZoneLabel: Record<string, string> = {
  FISH_HEAD: '🐟 Fish Head',
  FISH_BODY: '🐟 Fish Body',
  FISH_TAIL_LOW: '🐟 Fish Tail Low',
  FISH_TAIL_HIGH: '🐟 Fish Tail High',
  FISH_BONE: '🦴 Fish Bone',
  BONE_BROKEN: '💀 Bone Broken',
};

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
          {valuation.price?.toLocaleString(undefined, { minimumFractionDigits: 2 }) ?? '—'}
        </span>
      </div>

      {/* Net value subtitle */}
      <div className="text-sm text-[var(--text-secondary)]">
        Net Value: <span className="text-[var(--text-primary)] font-semibold tabular-nums font-mono">
          NT$ {valuation.net_value?.toLocaleString(undefined, { minimumFractionDigits: 2 }) ?? '—'}
        </span>
      </div>
    </div>
  );
};
