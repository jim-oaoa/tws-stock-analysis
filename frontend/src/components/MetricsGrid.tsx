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

export const MetricsGrid: React.FC<MetricsGridProps> = ({ valuation, fundamentalZone }) => {
  const fundColor = zoneColorMap[fundamentalZone] || 'var(--warning)';
  const valColor = valuationZoneColorMap[valuation.current_zone] || 'var(--text-secondary)';

  const cells = [
    { label: 'Current Price', value: `NT$ ${valuation.price?.toLocaleString(undefined, { minimumFractionDigits: 2 }) ?? '—'}`, mono: true },
    { label: 'Net Value', value: `NT$ ${valuation.net_value?.toLocaleString(undefined, { minimumFractionDigits: 2 }) ?? '—'}`, mono: true },
    { label: 'Fundamental Zone', value: fundamentalZone?.replace('_', ' ') || 'N/A', color: fundColor, badge: true },
    { label: 'Valuation Zone', value: valuation.current_zone?.replace('_', ' ') || 'N/A', color: valColor, badge: true },
  ];

  return (
    <div className="bg-[var(--bg-surface)] rounded-[var(--radius-lg)] border border-[var(--border-default)] shadow-[var(--elevation-1)] transition-all duration-[var(--duration-normal)] ease-[var(--easing)] hover:-translate-y-0.5 hover:shadow-[var(--elevation-2)]">
      <div className="p-5 pb-3">
        <h3 className="text-xs font-semibold text-[var(--text-secondary)] uppercase tracking-wider">
          Current Metrics
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
