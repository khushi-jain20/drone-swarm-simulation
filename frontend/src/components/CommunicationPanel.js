// frontend/src/components/CommunicationPanel.js
import React, { useEffect, useRef } from 'react';

const CommunicationPanel = ({ logs }) => {
    const logContainerRef = useRef(null);

    // Filter for only communication-related events
    const commLogs = logs?.filter(log => log.message.includes('shared')) ?? [];

    /*// Auto-scroll logic
    useEffect(() => {
        if (logContainerRef.current) {
            logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
        }
    }, [commLogs]);*/

    return (
        <div className="bg-gray-800 p-4 rounded-lg h-1/2 flex flex-col">
            <h2 className="text-xl font-bold mb-2 border-b border-gray-600 pb-2">Communication Log</h2>
            <div ref={logContainerRef} className="overflow-y-auto flex-grow">
                {commLogs.length > 0 ? (
                    commLogs.map((log, index) => (
                        <p key={index} className="text-sm">
                            <span className="text-gray-500">{log.time.toFixed(1)}s:</span>
                            <span className="text-cyan-400"> {log.message}</span>
                        </p>
                    ))
                ) : (
                    <p className="text-gray-500">Awaiting transmissions...</p>
                )}
            </div>
        </div>
    );
};

export default CommunicationPanel;