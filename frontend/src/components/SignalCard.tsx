import React from 'react';
import type { HybridSignal } from '../types/valuation';

interface SignalCardProps {
  signal: HybridSignal | undefined;
  action: string | undefined;
}

const signalConfig: Record<string, { color: string; bg: string; border: string }> = {
  STRONG_BUY: { color: '#22c55e', bg: 'rgba(34, 197, 94, 0.08)', border: 'rgba(34, 197, 94, 0.4)' },
  BUY: { color: '#22c55e', bg: 'rgba(34, 197, 94, 0.08)', border: 'rgba(34, 197, 94, 0.4)' },
  HOLD: { color: '#d29922', bg: 'rgba(210, 153, 34, 0.08)', border: 'rgba(210, 153, 34, 0.4)' },
  SELL: { color: '#ef4444', bg: 'rgba(239, 68, 68, 0.08)', border: 'rgba(239, 68, 68, 0.4)' },
  STRONG_SELL: { color: '#ef4444', bg: 'rgba(239, 68, 68, 0.08)', border: 'rgba(239, 68, 68, 0.4)' },
};

export const SignalCard: React.FC<SignalCardProps> = ({ signal, action }) => {
  const config = signal ? signalConfig[signal] : signalConfig.HOLD;

  return (
    <div
      className="relative rounded-[var(--radius-xl)] border p-6 backdrop-blur-sm transition-all duration-[var(--duration-normal)] ease-[var(--easing)] hover:-translate-y-0.5 hover:shadow-[var(--elevation-2)]"
      style={{
        backgroundColor: config.bg,
        borderColor: config.border,
        boxShadow: 'var(--elevation-1)',
      }}
    >
      {/* Animated pulse ring */}
      <div
        className="absolute inset-0 rounded-[var(--radius-xl)] pointer-events-none"
        style={{
          animation: 'pulse-ring 2s ease-out infinite',
          borderColor: config.color,
        }}
      />

      <div className="text-xs uppercase tracking-widest font-semibold text-[var(--text-secondary)] mb-1">
        Hybrid Signal
      </div>
      <div
        className="text-4xl md:text-5xl font-black mb-5"
        style={{ color: config.color }}
      >
        {signal?.replace('_', ' ') || 'N/A'}
      </div>

      {/* Divider */}
      <div
        className="border-t mb-4"
        style={{ borderColor: 'rgba(255,255,255,0.08)' }}
      />

      <div className="space-y-1">
        <div className="text-xs text-[var(--text-secondary)] uppercase tracking-wider">
          Recommended Action
        </div>
        <div className="text-lg font-semibold text-[var(--text-primary)]">
          {action || 'N/A'}
        </div>
      </div>
    </div>
  );
};
