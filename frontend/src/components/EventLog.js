// src/components/EventLog.js
import React, { useEffect, useRef } from 'react';

const EventLog = ({ logs }) => {
    const logContainerRef = useRef(null);

    // Automatically scroll to the bottom when new logs arrive
    useEffect(() => {
        if (logContainerRef.current) {
            logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
        }
    }, [logs]);

    return (
        <div className="bg-gray-800 p-4 rounded-lg h-1/2 flex flex-col">
            <h2 className="text-xl font-bold mb-2 border-b border-gray-600 pb-2">Event Log</h2>
            <div ref={logContainerRef} className="overflow-y-auto flex-grow">
                {/* Use optional chaining here to prevent crash if logs is undefined */}
                {logs?.length > 0 ? (
                    logs.map((log, index) => (
                        <p key={index} className="text-sm">
                            <span className="text-gray-500">{log.time.toFixed(2)}s:</span> {log.message}
                        </p>
                    ))
                ) : (
                    <p className="text-gray-500">No events yet...</p>
                )}
            </div>
        </div>
    );
};

export default EventLog;