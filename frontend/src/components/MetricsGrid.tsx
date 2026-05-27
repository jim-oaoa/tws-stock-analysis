import React from 'react';
import type { ValuationResult, FundamentalZone } from '../types/valuation';

interface MetricsGridProps {
  valuation: ValuationResult;
  fundamentalZone: FundamentalZone;
}

const zoneColorMap: Record<string, string> = {
  UNDERVALUED: 'var(--profit)',
  FAIR: 'var(--warning)',
  OVERVALUED: 'var(--loss)',
  BUBBLE: 'var(--loss)',
};

const valuationZoneColorMap: Record<string, string> = {
  FISH_HEAD: 'var(--fish-head)',
  FISH_BODY: 'var(--fish-body)',
  FISH_TAIL_LOW: 'var(--fish-tail)',
  FISH_TAIL_HIGH: 'var(--fish-tail)',
  FISH_BONE: 'var(--fish-bone)',
  BONE_BROKEN: 'var(--bone-broken)',
};

const fundamentalZoneLabelMap: Record<string, string> = {
  UNDERVALUED: '低估',
  FAIR: '合理',
  OVERVALUED: '高估',
  BUBBLE: '泡沫',
};

const valuationZoneLabelMap: Record<string, string> = {
  FISH_HEAD: '魚頭',
  FISH_BODY: '魚身',
  FISH_TAIL_LOW: '魚尾低',
  FISH_TAIL_HIGH: '魚尾高',
  FISH_BONE: '魚骨',
  BONE_BROKEN: '斷骨',
};

function formatNetValue(value: number): string {
  if (value >= 1e12) return `NT$ ${(value / 1e12).toFixed(2)} 兆`;
  if (value >= 1e8) return `NT$ ${(value / 1e8).toFixed(2)} 億`;
  return `NT$ ${value.toLocaleString(undefined, { maximumFractionDigits: 0 })}`;
}

export const MetricsGrid: React.FC<MetricsGridProps> = ({ valuation, fundamentalZone }) => {
  const fundColor = zoneColorMap[fundamentalZone] || 'var(--warning)';
  const valColor = valuationZoneColorMap[valuation.current_zone] || 'var(--text-secondary)';

  const fundZoneDisplay = fundamentalZoneLabelMap[fundamentalZone] || fundamentalZone?.replace('_', ' ') || '無';
  const valZoneDisplay = valuationZoneLabelMap[valuation.current_zone] || valuation.current_zone?.replace('_', ' ') || '無';

  const cells = [
    { label: '目前股價', value: `NT$ ${valuation.price?.toLocaleString(undefined, { maximumFractionDigits: 0 }) ?? '—'}`, mono: true },
    { label: '淨值', value: valuation.net_value != null ? formatNetValue(valuation.net_value) : '—', mono: true },
    { label: '基本面區間', value: fundZoneDisplay, color: fundColor, badge: true },
    { label: '估值區間', value: valZoneDisplay, color: valColor, badge: true },
  ];

  return (
    <div className="bg-[var(--bg-surface)] rounded-[var(--radius-lg)] border border-[var(--border-default)] shadow-[var(--elevation-1)] transition-all duration-[var(--duration-normal)] ease-[var(--easing)] hover:-translate-y-0.5 hover:shadow-[var(--elevation-2)]">
      <div className="p-5 pb-3">
        <h3 className="text-xs font-semibold text-[var(--text-secondary)] uppercase tracking-wider">
          目前指標
        </h3>
      </div>
      <div className="grid grid-cols-2">
        {cells.map((cell, i) => (
          <div
            key={cell.label}
            className="px-5 py-4 border-b border-r border-[var(--border-default)] transition-colors duration-[var(--duration-fast)] hover:bg-[var(--bg-elevated)]"
            style={{ borderRightWidth: i % 2 === 0 ? '1px' : '0' }}
          >
            <div className="text-xs text-[var(--text-secondary)] mb-1.5">{cell.label}</div>
            {cell.badge ? (
              <span
                className="inline-flex px-2 py-0.5 rounded-[var(--radius-sm)] text-xs font-semibold"
                style={{ color: cell.color, backgroundColor: `${cell.color}18` }}
              >
                {cell.value}
              </span>
            ) : (
              <div className={`text-lg font-bold text-[var(--text-primary)] ${cell.mono ? 'tabular-nums font-mono' : ''}`}>
                {cell.value}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
