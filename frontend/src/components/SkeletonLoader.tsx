import React from 'react';

/* === Skeleton Loading Components === */

export const SkeletonPrice: React.FC = () => (
  <div className="rounded-[var(--radius-xl)] border border-[var(--border-default)] p-6 md:p-8 animate-pulse">
    <div className="w-24 h-5 bg-[var(--bg-elevated)] rounded mb-4" />
    <div className="w-48 h-10 bg-[var(--bg-elevated)] rounded mb-3" />
    <div className="w-36 h-4 bg-[var(--bg-elevated)] rounded" />
  </div>
);

export const SkeletonChart: React.FC = () => (
  <div className="w-full h-[400px] rounded-[var(--radius-lg)] bg-[var(--bg-surface)] border border-[var(--border-default)] p-5 animate-pulse">
    <div className="w-32 h-4 bg-[var(--bg-elevated)] rounded mb-4" />
    <div className="w-full h-[calc(100%-2rem)] bg-[var(--bg-elevated)] rounded" />
  </div>
);

export const SkeletonTable: React.FC<{ rows?: number }> = ({ rows = 7 }) => (
  <div className="rounded-[var(--radius-lg)] border border-[var(--border-default)] overflow-hidden animate-pulse">
    <div className="px-6 py-4 border-b border-[var(--border-default)]">
      <div className="w-40 h-4 bg-[var(--bg-elevated)] rounded" />
    </div>
    <div className="p-4 space-y-2">
      {Array.from({ length: rows }, (_, i) => (
        <div key={i} className="flex gap-4">
          <div className="w-20 h-4 bg-[var(--bg-elevated)] rounded" />
          <div className="w-16 h-4 bg-[var(--bg-elevated)] rounded" />
          <div className="w-16 h-4 bg-[var(--bg-elevated)] rounded" />
          <div className="w-16 h-4 bg-[var(--bg-elevated)] rounded" />
          <div className="w-16 h-4 bg-[var(--bg-elevated)] rounded" />
          <div className="w-24 h-4 bg-[var(--accent-blue)]/20 rounded" />
        </div>
      ))}
    </div>
  </div>
);

export const SkeletonCard: React.FC = () => (
  <div className="rounded-[var(--radius-lg)] border border-[var(--border-default)] p-5 animate-pulse space-y-3">
    <div className="w-28 h-3 bg-[var(--bg-elevated)] rounded" />
    <div className="w-36 h-5 bg-[var(--bg-elevated)] rounded" />
    <div className="w-24 h-3 bg-[var(--bg-elevated)] rounded" />
  </div>
);

export const SkeletonSignal: React.FC = () => (
  <div
    className="rounded-[var(--radius-xl)] border p-6 animate-pulse"
    style={{ borderColor: 'rgba(255,255,255,0.08)', backgroundColor: 'rgba(255,255,255,0.02)' }}
  >
    <div className="w-24 h-3 bg-[var(--bg-elevated)] rounded mb-3" />
    <div className="w-44 h-9 bg-[var(--bg-elevated)] rounded mb-5" />
    <div className="border-t border-[var(--border-default)] pt-4">
      <div className="w-28 h-3 bg-[var(--bg-elevated)] rounded mb-2" />
      <div className="w-36 h-5 bg-[var(--bg-elevated)] rounded" />
    </div>
  </div>
);
