import React from 'react';

/* === Skeleton Loading Components — glass style === */

export const SkeletonPrice: React.FC = () => (
  <div className="glass-card rounded-[var(--radius-xl)] p-6 md:p-8 animate-pulse">
    <div className="w-24 h-5 bg-white/[0.06] rounded mb-4" />
    <div className="w-48 h-10 bg-white/[0.06] rounded mb-3" />
    <div className="w-36 h-4 bg-white/[0.06] rounded" />
  </div>
);

export const SkeletonChart: React.FC = () => (
  <div className="w-full h-[400px] rounded-[var(--radius-lg)] p-5 animate-pulse" style={{ backgroundColor: 'rgba(10, 10, 10, 0.6)' }}>
    <div className="w-32 h-4 bg-white/[0.06] rounded mb-4" />
    <div className="w-full h-[calc(100%-2rem)] bg-white/[0.06] rounded" />
  </div>
);

export const SkeletonTable: React.FC<{ rows?: number }> = ({ rows = 7 }) => (
  <div className="glass-card rounded-[var(--radius-lg)] overflow-hidden animate-pulse">
    <div className="px-6 py-4 border-b border-white/5">
      <div className="w-40 h-4 bg-white/[0.06] rounded" />
    </div>
    <div className="p-4 space-y-2">
      {Array.from({ length: rows }, (_, i) => (
        <div key={i} className="flex gap-4">
          <div className="w-20 h-4 bg-white/[0.06] rounded" />
          <div className="w-16 h-4 bg-white/[0.06] rounded" />
          <div className="w-16 h-4 bg-white/[0.06] rounded" />
          <div className="w-16 h-4 bg-white/[0.06] rounded" />
          <div className="w-16 h-4 bg-white/[0.06] rounded" />
          <div className="w-24 h-4 rounded" style={{ backgroundColor: 'rgba(232, 186, 64, 0.15)' }} />
        </div>
      ))}
    </div>
  </div>
);

export const SkeletonCard: React.FC = () => (
  <div className="glass-card rounded-[var(--radius-lg)] p-5 animate-pulse space-y-3">
    <div className="w-28 h-3 bg-white/[0.06] rounded" />
    <div className="w-36 h-5 bg-white/[0.06] rounded" />
    <div className="w-24 h-3 bg-white/[0.06] rounded" />
  </div>
);

export const SkeletonSignal: React.FC = () => (
  <div className="glass-card rounded-[var(--radius-xl)] p-6 animate-pulse">
    <div className="w-24 h-3 bg-white/[0.06] rounded mb-3" />
    <div className="w-44 h-9 bg-white/[0.06] rounded mb-5" />
    <div className="border-t border-white/5 pt-4">
      <div className="w-28 h-3 bg-white/[0.06] rounded mb-2" />
      <div className="w-36 h-5 bg-white/[0.06] rounded" />
    </div>
  </div>
);
