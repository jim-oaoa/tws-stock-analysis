import React, { Component, type ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('ErrorBoundary caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="bg-zinc-800 border border-rose-500/50 p-6 rounded-xl text-center">
          <div className="text-rose-500 text-3xl mb-3">⚠️</div>
          <h3 className="text-lg font-bold text-zinc-200 mb-2">Chart Error</h3>
          <p className="text-zinc-400 text-sm">{this.state.error?.message}</p>
        </div>
      );
    }
    return this.props.children;
  }
}
