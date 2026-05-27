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
              Fish-Bone Valuation
            </h1>
            <p className="text-xs md:text-sm text-[var(--text-secondary)]">
              Taiwan Stock Fundamental Dashboard
            </p>
          </div>
        </div>

        {/* Live indicator dot */}
        <div className="flex items-center gap-1.5 ml-2">
          <span
            className="inline-block w-2 h-2 rounded-full bg-[var(--profit)]"
            style={{ animation: 'pulse-dot 2s ease-in-out infinite' }}
            aria-label="System live"
          />
          <span className="text-[10px] uppercase tracking-widest text-[var(--text-dim)]">Live</span>
        </div>
      </div>

      {/* Search form */}
      <form onSubmit={onSearch} className="flex gap-2 w-full md:w-auto">
        <input
          type="text"
          value={symbol}
          onChange={(e) => onChange(e.target.value)}
          disabled={isLoading}
          className="flex-1 md:w-64 bg-[var(--bg-input)] border border-[var(--border-default)] rounded-full px-5 py-2.5 text-sm text-[var(--text-primary)] placeholder:text-[var(--text-dim)] focus:outline-none focus:ring-2 focus:ring-[var(--accent-blue)] focus:border-transparent transition-all duration-[var(--duration-fast)] ease-[var(--easing)]"
          placeholder="e.g. 2330.TW"
          aria-label="Stock symbol"
        />
        <button
          type="submit"
          disabled={isLoading}
          className="bg-[var(--accent-blue)] hover:bg-blue-500 text-white px-6 py-2.5 rounded-full font-medium text-sm transition-all duration-[var(--duration-fast)] ease-[var(--easing)] active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Loading...' : 'Analyze'}
        </button>
      </form>
    </header>
  );
};
