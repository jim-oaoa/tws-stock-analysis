import { useState, useEffect } from 'react';
import { fetchValuation, fetchSignal } from './api/valuation';
import { ValuationApiResponse, HybridSignalResult, HybridSignal } from './types/valuation';
import { ValuationChart } from './components/ValuationChart';
import './App.css';

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
    setSymbol(inputSymbol.toUpperCase());
  };

  const getSignalColor = (sig: HybridSignal | undefined) => {
    switch (sig) {
      case 'STRONG_BUY':
      case 'BUY':
        return 'text-emerald-400 border-emerald-400 bg-emerald-400/10';
      case 'STRONG_SELL':
      case 'SELL':
        return 'text-rose-400 border-rose-400 bg-rose-400/10';
      default:
        return 'text-amber-400 border-amber-400 bg-amber-400/10';
    }
  };

  // Transform quarterly_grid to chart data
  const chartData = valuation?.quarterly_grid.map(cell => ({
    time: `${cell.year}-Q${cell.quarter}`,
    value: cell.accumulated_net_value
  })) || [];

  if (loading) {
    return (
      <div className="min-h-screen bg-zinc-900 text-zinc-100 flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-zinc-700 border-t-blue-500 rounded-full animate-spin"></div>
          <p className="text-zinc-400 animate-pulse">Fetching valuation data for {symbol}...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-zinc-900 text-zinc-100 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-zinc-800 border border-rose-500/50 p-6 rounded-xl text-center">
          <div className="text-rose-500 text-4xl mb-4">⚠️</div>
          <h2 className="text-xl font-bold mb-2">Data Fetch Error</h2>
          <p className="text-zinc-400 mb-6">{error}</p>
          <button 
            onClick={() => setSymbol(symbol)} 
            className="px-4 py-2 bg-zinc-700 hover:bg-zinc-600 rounded-lg transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-zinc-900 text-zinc-100 p-4 md:p-8 font-sans">
      <div className="max-w-7xl mx-auto space-y-6">
        
        {/* Header & Search */}
        <header className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Fish-Bone Valuation</h1>
            <p className="text-zinc-400">Fundamental & Technical Analysis Dashboard</p>
          </div>
          <form onSubmit={handleSearch} className="flex gap-2">
            <input 
              type="text" 
              value={inputSymbol} 
              onChange={(e) => setInputSymbol(e.target.value)}
              className="bg-zinc-800 border border-zinc-700 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
              placeholder="Enter Symbol (e.g. 2330.TW)"
            />
            <button 
              type="submit" 
              className="bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded-lg font-medium transition-colors"
            >
              Analyze
            </button>
          </form>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Signal Dashboard */}
          <div className="lg:col-span-1 space-y-6">
            <div className={`p-6 rounded-2xl border-2 transition-all ${getSignalColor(signal?.final_signal)}`}>
              <div className="text-sm uppercase tracking-widest font-semibold opacity-80 mb-1">Hybrid Signal</div>
              <div className="text-4xl font-black mb-4">{signal?.final_signal?.replace('_', ' ') || 'N/A'}</div>
              <div className="pt-4 border-t border-current/20">
                <div className="text-sm opacity-80 mb-1">Recommended Action</div>
                <div className="text-lg font-medium">{signal?.action || 'N/A'}</div>
              </div>
            </div>

            <div className="bg-zinc-800 p-6 rounded-2xl border border-zinc-700 space-y-4">
              <h3 className="text-sm font-semibold text-zinc-400 uppercase tracking-wider">Current Metrics</h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1">
                  <div className="text-xs text-zinc-500">Current Price</div>
                  <div className="text-xl font-bold">${valuation?.valuation.price.toLocaleString()}</div>
                </div>
                <div className="space-y-1">
                  <div className="text-xs text-zinc-500">Net Value</div>
                  <div className="text-xl font-bold">${valuation?.valuation.net_value.toLocaleString()}</div>
                </div>
                <div className="space-y-1">
                  <div className="text-xs text-zinc-500">Fundamental Zone</div>
                  <div className="text-sm font-medium text-blue-400">{valuation?.fundamental_zone || 'N/A'}</div>
                </div>
                <div className="space-y-1">
                  <div className="text-xs text-zinc-500">Valuation Zone</div>
                  <div className="text-sm font-medium text-purple-400">{valuation?.valuation.current_zone || 'N/A'}</div>
                </div>
              </div>
            </div>
          </div>

          {/* Chart Section */}
          <div className="lg:col-span-2">
            <div className="bg-zinc-800 p-6 rounded-2xl border border-zinc-700 h-full">
              <h3 className="text-sm font-semibold text-zinc-400 uppercase tracking-wider mb-4">Valuation Curve</h3>
              {valuation && (
                <ValuationChart 
                  data={chartData} 
                  valuation={valuation.valuation} 
                />
              )}
            </div>
          </div>
        </div>

        {/* Data Table Section */}
        <div className="bg-zinc-800 rounded-2xl border border-zinc-700 overflow-hidden">
          <div className="p-6 border-b border-zinc-700">
            <h3 className="text-sm font-semibold text-zinc-400 uppercase tracking-wider">Quarterly Valuation Grid</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-zinc-900/50 text-zinc-400 text-xs uppercase tracking-wider">
                  <th className="px-6 py-3 font-medium border-b border-zinc-700">Period</th>
                  <th className="px-6 py-3 font-medium border-b border-zinc-700 text-right">EPS</th>
                  <th className="px-6 py-3 font-medium border-b border-zinc-700 text-right">OCI</th>
                  <th className="px-6 py-3 font-medium border-b border-zinc-700 text-right">Dividends</th>
                  <th className="px-6 py-3 font-medium border-b border-zinc-700 text-right">Adjustment</th>
                  <th className="px-6 py-3 font-medium border-b border-zinc-700 text-right text-blue-400">Accum. Net Value</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-700">
                {valuation?.quarterly_grid.map((cell, idx) => (
                  <tr key={idx} className="hover:bg-zinc-700/30 transition-colors text-sm">
                    <td className="px-6 py-3 font-medium">{cell.year} Q{cell.quarter}</td>
                    <td className="px-6 py-3 text-right">{cell.eps.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
                    <td className="px-6 py-3 text-right">{cell.oci.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
                    <td className="px-6 py-3 text-right">{cell.dividends.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
                    <td className="px-6 py-3 text-right">{cell.adjustment_amount.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
                    <td className="px-6 py-3 text-right font-bold text-blue-400">{cell.accumulated_net_value.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
