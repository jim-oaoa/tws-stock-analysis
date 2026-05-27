import React from 'react';
import type { QuarterlyGridCell } from '../types/valuation';

interface QuarterlyTableProps {
  grid: QuarterlyGridCell[];
}

function formatNetValue(value: number): string {
  if (value >= 1e12) return `NT$ ${(value / 1e12).toFixed(2)} 兆`;
  if (value >= 1e8) return `NT$ ${(value / 1e8).toFixed(2)} 億`;
  return `NT$ ${value.toLocaleString(undefined, { maximumFractionDigits: 0 })}`;
}

function formatTableCell(value: number | undefined | null): string {
  if (value == null) return '0.00';
  return value.toLocaleString(undefined, { maximumFractionDigits: 0 });
}

export const QuarterlyTable: React.FC<QuarterlyTableProps> = ({ grid }) => {
  if (!grid || grid.length === 0) {
    return (
      <div className="bg-[var(--bg-surface)] rounded-[var(--radius-lg)] p-8 text-center shadow-[var(--elevation-1)]">
        <p className="text-[var(--text-secondary)] text-sm">尚無季度資料</p>
      </div>
    );
  }

  return (
    <div className="bg-[var(--bg-surface)] rounded-[var(--radius-lg)] shadow-[var(--elevation-1)] overflow-hidden">
      <div className="px-6 py-4 border-b" style={{ borderColor: 'var(--divider)' }}>
        <h3 className="text-sm font-semibold text-[var(--text-secondary)] uppercase tracking-wider">
          季度估值表
        </h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr
              className="text-xs uppercase tracking-wider"
              style={{
                backgroundColor: 'rgba(0, 0, 0, 0.3)',
                color: 'var(--text-secondary)',
                position: 'sticky',
                top: 0,
                zIndex: 10,
              }}
            >
              <th className="px-6 py-3 font-medium border-b whitespace-nowrap" style={{ borderColor: 'var(--divider)' }}>期間</th>
              <th className="px-6 py-3 font-medium border-b text-right whitespace-nowrap" style={{ borderColor: 'var(--divider)' }}>每股盈餘</th>
              <th className="px-6 py-3 font-medium border-b text-right whitespace-nowrap" style={{ borderColor: 'var(--divider)' }}>其他損益</th>
              <th className="px-6 py-3 font-medium border-b text-right whitespace-nowrap" style={{ borderColor: 'var(--divider)' }}>股利</th>
              <th className="px-6 py-3 font-medium border-b text-right whitespace-nowrap" style={{ borderColor: 'var(--divider)' }}>調整</th>
              <th
                className="px-6 py-3 font-medium border-b text-right whitespace-nowrap"
                style={{ color: 'var(--accent-blue)', borderColor: 'var(--divider)' }}
              >
                累積淨值
              </th>
            </tr>
          </thead>
          <tbody className="divide-y" style={{ '--tw-divide-y-reverse': 0, borderColor: 'var(--divider)' } as React.CSSProperties}>
            {grid.map((cell, idx) => (
              <tr
                key={`${cell.year}-${cell.quarter}`}
                className="text-sm transition-colors duration-[var(--duration-fast)] hover:bg-[var(--bg-elevated)]"
                style={{
                  backgroundColor: idx % 2 === 0 ? 'var(--bg-surface)' : 'rgba(34, 34, 38, 0.4)',
                }}
              >
                <td className="px-6 py-3 font-medium text-[var(--text-primary)] whitespace-nowrap">
                  {cell.year} Q{cell.quarter}
                </td>
                <td className="px-6 py-3 text-right text-[var(--text-primary)] tabular-nums font-mono whitespace-nowrap">
                  {formatTableCell(cell.eps)}
                </td>
                <td className="px-6 py-3 text-right text-[var(--text-primary)] tabular-nums font-mono whitespace-nowrap">
                  {formatTableCell(cell.oci)}
                </td>
                <td className="px-6 py-3 text-right text-[var(--text-primary)] tabular-nums font-mono whitespace-nowrap">
                  {cell.dividends != null ? formatNetValue(cell.dividends) : '—'}
                </td>
                <td className="px-6 py-3 text-right text-[var(--text-primary)] tabular-nums font-mono whitespace-nowrap">
                  {formatTableCell(cell.adjustment_amount)}
                </td>
                <td
                  className="px-6 py-3 text-right font-semibold tabular-nums font-mono whitespace-nowrap"
                  style={{ color: 'var(--accent-blue)' }}
                >
                  {cell.accumulated_net_value != null ? formatNetValue(cell.accumulated_net_value) : '—'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
