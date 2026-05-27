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
        <div className="p-6 rounded-[var(--radius-lg)] text-center shadow-[var(--elevation-1)]" style={{ backgroundColor: 'var(--loss-dim)', border: '1px solid var(--loss)' }}>
          <div className="text-3xl mb-3" style={{ color: 'var(--loss)' }}>⚠️</div>
          <h3 className="text-lg font-semibold text-[var(--text-primary)] mb-2" style={{ letterSpacing: '-0.02em' }}>Chart Error</h3>
          <p className="text-sm text-[var(--text-secondary)]">{this.state.error?.message}</p>
        </div>
      );
    }
    return this.props.children;
  }
}
