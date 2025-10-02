// src/components/MetricsPanel.js
import React from 'react';

const MetricItem = ({ label, value }) => (
    <div className="flex justify-between text-lg">
        <span className="text-gray-400">{label}:</span>
        <span className="text-cyan-400">{value}</span>
    </div>
);

// This component receives the `metrics` object as a prop from App.js
const MetricsPanel = ({ metrics }) => {
    // --- SOLUTION ---
    // We use optional chaining (?.) and the nullish coalescing operator (??)
    // This safely handles cases where metrics or its properties might not exist yet.
    // It says "try to access the value, but if it's null or undefined, use 0 instead."

    return (
        <div className="bg-gray-800 p-4 rounded-lg h-full flex flex-col">
            <h2 className="text-xl font-bold mb-4 border-b border-gray-600 pb-2">Live Metrics</h2>
            <div className="flex flex-col gap-2">
                <MetricItem label="Assets Saved" value={metrics?.assets_saved ?? 0} />
                <MetricItem label="Neutralizations" value={metrics?.neutralizations ?? 0} />
                <MetricItem label="Friendly Losses" value={metrics?.friendly_losses ?? 0} />
                <MetricItem 
                    label="Avg Intercept Time" 
                    value={`${(metrics?.avg_interception_time ?? 0).toFixed(2)}s`} // This line is now safe
                />
                <MetricItem 
                    label="% Unattended Hostiles" 
                    value={`${metrics?.percent_unattended_hostiles ?? 0}%`} 
                />
            </div>
        </div>
    );
};

export default MetricsPanel;