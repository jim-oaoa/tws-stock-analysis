import { useState, useEffect } from 'react';
import { fetchValuation, fetchSignal } from './api/valuation';
import type { ValuationApiResponse, HybridSignalResult } from './types/valuation';
import { ErrorBoundary } from './components/ErrorBoundary';
import { Header } from './components/Header';
import { PriceHero } from './components/PriceHero';
import { SignalCard } from './components/SignalCard';
import { MetricsGrid } from './components/MetricsGrid';
import { TechnicalCard } from './components/TechnicalCard';
import { QuarterlyTable } from './components/QuarterlyTable';
import { ValuationChart } from './components/ValuationChart';
import { SkeletonPrice, SkeletonChart, SkeletonTable, SkeletonSignal, SkeletonCard } from './components/SkeletonLoader';
import { ErrorCard } from './components/ErrorCard';

function App() {
  const [symbol, setSymbol] = useState('2330.TW');
  const [inputSymbol, setInputSymbol] = useState('2330.TW');
  const [valuation, setValuation] = useState<ValuationApiResponse | null>(null);
  const [signal, setSignal] = useState<HybridSignalResult | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [valuationData, signalData] = await Promise.all([
          fetchValuation(symbol),
          fetchSignal(symbol),
        ]);
        setValuation(valuationData);
        setSignal(signalData);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError(err instanceof Error ? err.message : 'An unknown error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [symbol]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = inputSymbol.trim().toUpperCase();
    if (trimmed) {
      setSymbol(trimmed);
    }
  };

  const handleRetry = () => {
    setSymbol(symbol);
  };

  // Transform quarterly_grid to chart data with proper yyyy-mm-dd format.
  // lightweight-charts requires: (1) yyyy-mm-dd format, (2) ascending time order.
  // API returns newest-first; we reverse to oldest-first.
  const chartData = (valuation?.quarterly_grid || [])
    .map(cell => {
      const quarterToMonth: Record<number, string> = { 1: '03-31', 2: '06-30', 3: '09-30', 4: '12-31' };
      return {
        time: `${cell.year}-${quarterToMonth[cell.quarter] || '12-31'}`,
        value: cell.accumulated_net_value
      };
    })
    .reverse(); // lightweight-charts requires ascending (oldest → newest)

  // --- Loading state: Skeleton screens ---
  if (loading) {
    return (
      <div className="min-h-screen bg-[var(--bg-root)] text-[var(--text-primary)]">
        <Header
          symbol={inputSymbol}
          onSearch={() => {}}
          onChange={setInputSymbol}
          isLoading={true}
        />
        <div className="container space-y-8 py-10">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-1 space-y-6">
              <SkeletonSignal />
              <SkeletonCard />
              <SkeletonCard />
            </div>
            <div className="lg:col-span-2 space-y-6">
              <SkeletonPrice />
              <SkeletonChart />
            </div>
          </div>
          <SkeletonTable />
        </div>
      </div>
    );
  }

  // --- Error state: Card-level error with retry ---
  if (error) {
    return (
      <div className="min-h-screen bg-[var(--bg-root)] text-[var(--text-primary)]">
        <Header
          symbol={inputSymbol}
          onSearch={handleSearch}
          onChange={setInputSymbol}
          isLoading={false}
        />
        <div className="container py-10">
          <div className="animate-fade-in-up">
            <ErrorCard message={error} onRetry={handleRetry} />
          </div>
        </div>
      </div>
    );
  }

  // --- Main dashboard ---
  return (
    <div className="min-h-screen bg-[var(--bg-root)] text-[var(--text-primary)]">
      <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-[#e8ba40] focus:text-gray-950 focus:rounded-full">
        跳至主要內容
      </a>

      <Header
        symbol={inputSymbol}
        onSearch={handleSearch}
        onChange={setInputSymbol}
        isLoading={loading}
      />

      <div className="container space-y-8 py-10 pb-20">
        <main id="main-content" className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left sidebar: Signal + Metrics + Technical */}
          <section className="lg:col-span-1 space-y-6" aria-label="訊號與指標">
            <div className="animate-fade-in-up">
              <SignalCard
                signal={signal?.final_signal}
                action={signal?.action}
              />
            </div>
            {valuation && (
              <div className="animate-fade-in-up animate-delay-100">
                <MetricsGrid
                  valuation={valuation.valuation}
                  fundamentalZone={valuation.fundamental_zone}
                />
              </div>
            )}
            {signal?.technical && (
              <div className="animate-fade-in-up animate-delay-200">
                <TechnicalCard technical={signal.technical} />
              </div>
            )}
          </section>

          {/* Right column: Price Hero + Valuation Chart */}
          <section className="lg:col-span-2 space-y-6" aria-label="價格與圖表">
            {valuation && (
              <div className="animate-fade-in-up animate-delay-100">
                <PriceHero
                  valuation={valuation.valuation}
                  fundamentalZone={valuation.fundamental_zone}
                />
              </div>
            )}
            <div className="glass-card rounded-[var(--radius-lg)] p-5 animate-fade-in-up animate-delay-200">
              <h2 className="text-sm font-semibold text-[var(--text-secondary)] uppercase tracking-wider mb-4">
                估值曲線
              </h2>
              {valuation && chartData.length > 0 && (
                <ErrorBoundary>
                  <ValuationChart
                    data={chartData}
                    valuation={valuation.valuation}
                  />
                </ErrorBoundary>
              )}
              {(!chartData || chartData.length === 0) && (
                <div className="h-[400px] flex items-center justify-center text-[var(--text-secondary)] text-sm">
                  尚無圖表資料
                </div>
              )}
            </div>
          </section>
        </main>

        {/* Quarterly Table — full width */}
        <section aria-label="季度資料" className="animate-fade-in-up animate-delay-300">
          <QuarterlyTable grid={valuation?.quarterly_grid || []} />
        </section>
      </div>
    </div>
  );
}

export default App;
