import React, { useEffect, useRef } from 'react';
import { createChart, ColorType, LineSeries } from 'lightweight-charts';
import type { ISeriesApi } from 'lightweight-charts';
import type { ValuationResult } from '../types/valuation';

interface ValuationChartProps {
    data: { time: string; value: number }[];
    valuation: ValuationResult;
}

export const ValuationChart: React.FC<ValuationChartProps> = ({ data, valuation }) => {
    const chartContainerRef = useRef<HTMLDivElement>(null);
    const chartRef = useRef<any>(null);
    const seriesRef = useRef<ISeriesApi<"Line"> | null>(null);

    useEffect(() => {
        if (!chartContainerRef.current) return;

        const chart = createChart(chartContainerRef.current, {
            layout: {
                background: { type: ColorType.Solid, color: 'transparent' },
                textColor: '#9095a1',
            },
            grid: {
                vertLines: { color: 'rgba(255,255,255,0.04)' },
                horzLines: { color: 'rgba(255,255,255,0.04)' },
            },
            width: chartContainerRef.current.clientWidth,
            height: 400,
            crosshair: {
                mode: 0,
            },
            rightPriceScale: {
                borderColor: 'rgba(255,255,255,0.06)',
            },
            timeScale: {
                borderColor: 'rgba(255,255,255,0.06)',
                timeVisible: true,
                secondsVisible: false,
            },
        });

        const lineSeries = chart.addSeries(LineSeries, {
            color: '#0fedbe',
            lineWidth: 2,
            priceLineVisible: false,
        });

        lineSeries.setData(data);
        chartRef.current = chart;
        seriesRef.current = lineSeries;

        const handleResize = () => {
            if (chartContainerRef.current) {
                chart.applyOptions({ width: chartContainerRef.current.clientWidth });
            }
        };

        window.addEventListener('resize', handleResize);
        return () => {
            window.removeEventListener('resize', handleResize);
            chart.remove();
        };
    }, [data]);

    const priceLinesRef = useRef<any[]>([]);

    useEffect(() => {
        if (!seriesRef.current) return;

        // Remove old price lines to prevent duplicates on valuation update
        priceLinesRef.current.forEach(line => seriesRef.current?.removePriceLine(line));
        priceLinesRef.current = [];

        const zones = valuation.zones;
        const lineConfigs: Array<{
            price: number;
            color: string;
            lineWidth: 1 | 2 | 3 | 4;
            lineStyle: 0 | 1 | 2 | 3 | 4;
            axisLabelVisible: boolean;
            title: string;
        }> = [
            { price: zones.fish_head, color: '#22c55e', lineWidth: 1, lineStyle: 2, axisLabelVisible: true, title: '魚頭 (0.85x)' },
            { price: zones.fish_body, color: '#d29922', lineWidth: 2, lineStyle: 0, axisLabelVisible: true, title: '魚身 (1.00x)' },
            { price: zones.fish_tail_low, color: '#f0883e', lineWidth: 1, lineStyle: 2, axisLabelVisible: true, title: '魚尾低 (1.15x)' },
            { price: zones.fish_tail_high, color: '#ef4444', lineWidth: 1, lineStyle: 2, axisLabelVisible: true, title: '魚尾高 (1.30x)' },
            { price: zones.fish_bone, color: '#ef4444', lineWidth: 2, lineStyle: 0, axisLabelVisible: true, title: '魚骨 (2.00x)' },
        ];

        priceLinesRef.current = lineConfigs.map(config =>
            seriesRef.current!.createPriceLine(config)
        );
    }, [valuation]);

    return (
        <div
            className="relative w-full h-[400px] rounded-[var(--radius-md)]"
            style={{ backgroundColor: 'rgba(10, 10, 10, 0.6)' }}
        >
            <div ref={chartContainerRef} className="w-full h-full" />
            {/* Price overlay */}
            <div
                className="absolute top-3 right-3 px-3 py-1.5 rounded-[var(--radius-sm)] text-xs"
                style={{
                    backgroundColor: 'rgba(0, 0, 0, 0.6)',
                    color: 'var(--text-secondary)',
                    backdropFilter: 'blur(8px)',
                    border: '1px solid rgba(255, 255, 255, 0.06)',
                }}
            >
                目前：{' '}
                <span className="text-[var(--text-primary)] font-semibold tabular-nums">
                    NT$ {valuation.price?.toLocaleString(undefined, { maximumFractionDigits: 0 })}
                </span>
            </div>
        </div>
    );
};
