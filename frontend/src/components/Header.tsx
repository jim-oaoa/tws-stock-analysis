import React from 'react';

interface HeaderProps {
  symbol: string;
  onSearch: (e: React.FormEvent) => void;
  onChange: (value: string) => void;
  isLoading: boolean;
}

export const Header: React.FC<HeaderProps> = ({ symbol, onSearch, onChange, isLoading }) => {
  return (
    <header className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
      <div className="flex items-center gap-3">
        {/* Logo area */}
        <div className="flex items-center gap-2">
          <span className="text-2xl" role="img" aria-label="Fish-Bone">🐟</span>
          <div>
            <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-[var(--text-primary)]">
              魚骨估值儀表板
            </h1>
            <p className="text-xs md:text-sm text-[var(--text-secondary)]">
              台股基本面分析
            </p>
          </div>
        </div>

        {/* Live indicator dot */}
        <div className="flex items-center gap-1.5 ml-2">
          <span
            className="inline-block w-2 h-2 rounded-full bg-[var(--profit)]"
            style={{ animation: 'pulse-dot 2s ease-in-out infinite' }}
            aria-label="系統連線中"
          />
          <span className="text-[10px] uppercase tracking-widest text-[var(--text-dim)]">即時</span>
        </div>
      </div>

      {/* Search form */}
      <form onSubmit={onSearch} className="flex flex-col gap-1.5 w-full md:w-auto">
        <label htmlFor="stock-symbol" className="text-xs text-[var(--text-secondary)] font-medium ml-1">
          股票代號
        </label>
        <div className="flex gap-2">
          <input
            id="stock-symbol"
            type="text"
            value={symbol}
            onChange={(e) => onChange(e.target.value)}
            disabled={isLoading}
            className="flex-1 md:w-64 bg-[var(--bg-input)] border border-[var(--border-default)] rounded-full px-5 py-2.5 text-sm text-[var(--text-primary)] placeholder:text-[var(--text-dim)] focus:outline-none focus:ring-2 focus:ring-[var(--accent-blue)] focus:border-transparent transition-all duration-[var(--duration-fast)] ease-[var(--easing)]"
            placeholder="例如 2330.TW"
          />
          <button
            type="submit"
            disabled={isLoading}
            className="bg-[var(--accent-blue)] hover:bg-blue-500 text-white px-6 py-2.5 rounded-full font-medium text-sm transition-all duration-[var(--duration-fast)] ease-[var(--easing)] active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? '載入中...' : '分析'}
          </button>
        </div>
      </form>
    </header>
  );
};
