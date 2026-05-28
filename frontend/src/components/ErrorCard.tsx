import React from 'react';

interface ErrorCardProps {
  message: string;
  onRetry?: () => void;
}

export const ErrorCard: React.FC<ErrorCardProps> = ({ message, onRetry }) => {
  return (
    <div
      role="alert"
      aria-live="assertive"
      className="glass-card rounded-[var(--radius-lg)] p-6 text-center"
      style={{ borderColor: 'rgba(239, 68, 68, 0.25)' }}
    >
      <div className="text-3xl mb-3" role="img" aria-label="錯誤">⚠️</div>
      <h3 className="text-lg font-bold text-[var(--text-primary)] mb-2">
        發生錯誤
      </h3>
      <p className="text-sm text-[var(--text-secondary)] mb-5 max-w-md mx-auto">
        {message}
      </p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="inline-flex items-center gap-2 px-5 py-2 rounded-full text-sm font-semibold text-gray-950 transition-all duration-[var(--duration-fast)] ease-[var(--easing)] hover:bg-[#fdd458] active:scale-95"
          style={{
            backgroundColor: '#e8ba40',
            boxShadow: '0 0 20px -5px rgba(232, 186, 64, 0.3)',
          }}
        >
          重試
        </button>
      )}
    </div>
  );
};
