import { useState, useEffect, useRef } from 'react';

interface UseCountUpOptions {
  /** Target value to animate to */
  target: number;
  /** Duration in milliseconds (default: 500) */
  duration?: number;
  /** Whether to start animating immediately (default: true) */
  enabled?: boolean;
}

/**
 * Animates a number from 0 (or previous target) to the given target over the specified duration.
 * Uses requestAnimationFrame for smooth animation.
 * Respects prefers-reduced-motion: returns target instantly if set.
 */
export function useCountUp({ target, duration = 500, enabled = true }: UseCountUpOptions): number {
  const [current, setCurrent] = useState(target);
  const rafRef = useRef<number | null>(null);
  const startTimeRef = useRef<number | null>(null);
  const startValueRef = useRef<number>(current);

  useEffect(() => {
    // Check prefers-reduced-motion
    const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReduced || !enabled) {
      setCurrent(target);
      return;
    }

    // Cancel any in-flight animation
    if (rafRef.current !== null) {
      cancelAnimationFrame(rafRef.current);
    }

    startValueRef.current = current;
    startTimeRef.current = null;

    const animate = (timestamp: number) => {
      if (startTimeRef.current === null) {
        startTimeRef.current = timestamp;
      }

      const elapsed = timestamp - startTimeRef.current;
      const progress = Math.min(elapsed / duration, 1);

      // Ease-out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      const nextValue = startValueRef.current + (target - startValueRef.current) * eased;

      setCurrent(nextValue);

      if (progress < 1) {
        rafRef.current = requestAnimationFrame(animate);
      } else {
        setCurrent(target);
        rafRef.current = null;
      }
    };

    rafRef.current = requestAnimationFrame(animate);

    return () => {
      if (rafRef.current !== null) {
        cancelAnimationFrame(rafRef.current);
      }
    };
  }, [target, duration, enabled]);

  return current;
}
