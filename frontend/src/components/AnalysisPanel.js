// src/components/AnalysisPanel.js
import React from 'react';

const AnalysisPanel = ({ analysisData }) => {
    const targets = analysisData?.coordination_targets ?? [];
    return (
        <div className="bg-gray-800 p-4 rounded-lg h-1/2 flex flex-col">
            <h2 className="text-xl font-bold mb-2 border-b border-gray-600 pb-2">Coordination Targets</h2>
            <div className="overflow-y-auto">
                {targets.length > 0 ? (
                    targets.map((t, i) => (
                        <p key={i} className="text-base">
                            F:[<span className="text-cyan-400">{t.source_id.slice(-4)}</span>] → 
                            E:[<span className="text-red-400">{t.target_id.slice(-4)}</span>] 
                            @ {t.distance}m
                        </p>
                    ))
                ) : (
                    <p className="text-gray-500">No active engagements...</p>
                )}
            </div>
        </div>
    );
};

export default AnalysisPanel;