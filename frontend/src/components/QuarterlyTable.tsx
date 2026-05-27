import React from 'react';
import type { QuarterlyGridCell } from '../types/valuation';

interface QuarterlyTableProps {
  grid: QuarterlyGridCell[];
}

export const QuarterlyTable: React.FC<QuarterlyTableProps> = ({ grid }) => {
  if (!grid || grid.length === 0) {
    return (
      <div className="bg-[var(--bg-surface)] rounded-[var(--radius-lg)] border border-[var(--border-default)] p-8 text-center">
        <p className="text-[var(--text-dim)] text-sm">No quarterly data available</p>
      </div>
    );
  }

  return (
    <div className="bg-[var(--bg-surface)] rounded-[var(--radius-lg)] border border-[var(--border-default)] shadow-[var(--elevation-1)] overflow-hidden">
      <div className="px-6 py-4 border-b border-[var(--border-default)]">
        <h3 className="text-sm font-semibold text-[var(--text-secondary)] uppercase tracking-wider">
          Quarterly Valuation Grid
        </h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr
              className="text-xs uppercase tracking-wider"
              style={{
                backgroundColor: 'rgba(10, 14, 15, 0.5)',
                color: 'var(--text-secondary)',
                position: 'sticky',
                top: 0,
                zIndex: 10,
              }}
            >
              <th className="px-6 py-3 font-medium border-b border-[var(--border-default)] whitespace-nowrap">Period</th>
              <th className="px-6 py-3 font-medium border-b border-[var(--border-default)] text-right whitespace-nowrap">EPS</th>
              <th className="px-6 py-3 font-medium border-b border-[var(--border-default)] text-right whitespace-nowrap">OCI</th>
              <th className="px-6 py-3 font-medium border-b border-[var(--border-default)] text-right whitespace-nowrap">Dividends</th>
              <th className="px-6 py-3 font-medium border-b border-[var(--border-default)] text-right whitespace-nowrap">Adjustment</th>
              <th
                className="px-6 py-3 font-medium border-b border-[var(--border-default)] text-right whitespace-nowrap"
                style={{ color: 'var(--accent-blue)' }}
              >
                Accum. Net Value
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[var(--border-default)]">
            {grid.map((cell, idx) => (
              <tr
                key={`${cell.year}-${cell.quarter}`}
                className="text-sm transition-colors duration-[var(--duration-fast)] hover:bg-[var(--bg-elevated)]"
                style={{
                  backgroundColor: idx % 2 === 0 ? 'var(--bg-surface)' : 'rgba(26, 31, 36, 0.5)',
                }}
              >
                <td className="px-6 py-3 font-medium text-[var(--text-primary)] whitespace-nowrap">
                  {cell.year} Q{cell.quarter}
                </td>
                <td className="px-6 py-3 text-right text-[var(--text-primary)] tabular-nums font-mono whitespace-nowrap">
                  {cell.eps?.toLocaleString(undefined, { minimumFractionDigits: 2 }) ?? '0.00'}
                </td>
                <td className="px-6 py-3 text-right text-[var(--text-primary)] tabular-nums font-mono whitespace-nowrap">
                  {cell.oci?.toLocaleString(undefined, { minimumFractionDigits: 2 }) ?? '0.00'}
                </td>
                <td className="px-6 py-3 text-right text-[var(--text-primary)] tabular-nums font-mono whitespace-nowrap">
                  {cell.dividends?.toLocaleString(undefined, { minimumFractionDigits: 2 }) ?? '0.00'}
                </td>
                <td className="px-6 py-3 text-right text-[var(--text-primary)] tabular-nums font-mono whitespace-nowrap">
                  {cell.adjustment_amount?.toLocaleString(undefined, { minimumFractionDigits: 2 }) ?? '0.00'}
                </td>
                <td
                  className="px-6 py-3 text-right font-bold tabular-nums font-mono whitespace-nowrap"
                  style={{ color: 'var(--accent-blue)' }}
                >
                  {cell.accumulated_net_value?.toLocaleString(undefined, { minimumFractionDigits: 2 }) ?? '0.00'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
