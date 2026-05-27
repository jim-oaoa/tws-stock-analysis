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

        // 1. Initialize Chart
        const chart = createChart(chartContainerRef.current, {
            layout: {
                background: { type: ColorType.Solid, color: '#1a1a1a' },
                textColor: '#d1d5db',
            },
            grid: {
                vertLines: { color: '#333' },
                horzLines: { color: '#333' },
            },
            width: chartContainerRef.current.clientWidth,
            height: 400,
        });

        const lineSeries = chart.addSeries(LineSeries, {
            color: '#3b82f6',
            lineWidth: 2,
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
        const lineConfigs: Array<{ price: number; color: string; lineWidth: 1 | 2 | 3 | 4; lineStyle: 0 | 1 | 2 | 3 | 4; axisLabelVisible: boolean; title: string }> = [
            { price: zones.fish_head, color: '#22c55e', lineWidth: 1 as const, lineStyle: 2 as const, axisLabelVisible: true, title: 'Fish Head (0.85x)' },
            { price: zones.fish_body, color: '#eab308', lineWidth: 2 as const, lineStyle: 0 as const, axisLabelVisible: true, title: 'Fish Body (1.00x)' },
            { price: zones.fish_tail_low, color: '#f97316', lineWidth: 1 as const, lineStyle: 2 as const, axisLabelVisible: true, title: 'Fish Tail Low (1.15x)' },
            { price: zones.fish_tail_high, color: '#ef4444', lineWidth: 1 as const, lineStyle: 2 as const, axisLabelVisible: true, title: 'Fish Tail High (1.30x)' },
            { price: zones.fish_bone, color: '#7f1d1d', lineWidth: 2 as const, lineStyle: 0 as const, axisLabelVisible: true, title: 'Fish Bone (2.00x)' },
        ];

        priceLinesRef.current = lineConfigs.map(config => 
            seriesRef.current!.createPriceLine(config)
        );
    }, [valuation]);

    return (
        <div className="relative w-full h-[400px] bg-[#1a1a1a] rounded-lg p-4 border border-gray-800">
            <div ref={chartContainerRef} className="w-full h-full" />
            <div className="absolute top-4 right-4 bg-black/60 p-2 rounded text-xs text-gray-300 border border-gray-700">
                Current: <span className="text-white font-bold">{valuation.price}</span>
            </div>
        </div>
    );
};
