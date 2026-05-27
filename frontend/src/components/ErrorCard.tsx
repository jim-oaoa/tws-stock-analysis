import React from 'react';

interface ErrorCardProps {
  message: string;
  onRetry?: () => void;
}

export const ErrorCard: React.FC<ErrorCardProps> = ({ message, onRetry }) => {
  return (
    <div
      className="rounded-[var(--radius-lg)] border p-6 text-center"
      style={{
        backgroundColor: 'var(--loss-dim)',
        borderColor: 'var(--loss)',
      }}
    >
      <div className="text-3xl mb-3" role="img" aria-label="Error">⚠️</div>
      <h3 className="text-lg font-bold text-[var(--text-primary)] mb-2">
        Something went wrong
      </h3>
      <p className="text-sm text-[var(--text-secondary)] mb-5 max-w-md mx-auto">
        {message}
      </p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="inline-flex items-center gap-2 px-5 py-2 rounded-full text-sm font-medium text-white transition-all duration-[var(--duration-fast)] ease-[var(--easing)] hover:opacity-90 active:scale-95"
          style={{ backgroundColor: 'var(--loss)' }}
        >
          Try Again
        </button>
      )}
    </div>
  );
};
