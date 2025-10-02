// frontend/src/components/ControlPanel.js
import React, { useState } from 'react';

const ControlPanel = ({ status, onStart, onPause, onResume, onReset }) => {
    const [friendlyCount, setFriendlyCount] = useState(8);
    const [enemyCount, setEnemyCount] = useState(12);

    const sendConfig = async (endpoint, value) => {
        try {
            await fetch(`http://localhost:8000/config/${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(value),
            });
        } catch (error) { console.error(`Failed to set ${endpoint}:`, error); }
    };
    const setSpeed = (speed) => sendConfig('speed', { multiplier: speed });
    const setAiLevel = (level) => sendConfig('ai_level', { level: level });

    const handleStart = () => {
        onStart({
            num_friendly: parseInt(friendlyCount, 10),
            num_enemy: parseInt(enemyCount, 10),
        });
    };
    
    // --- FINAL & CORRECT BUTTON STATE LOGIC ---
    const isIdle = status === 'idle';
    const isRunning = status === 'running';
    const isPaused = status === 'paused';
    
    // Inputs and Start are disabled if the simulation is active in any way.
    const canStart = isIdle;

    return (
        <div className="bg-gray-800 p-4 rounded-lg flex flex-col gap-4">
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2">
                        <label htmlFor="friendly" className="font-bold text-cyan-400">Friendlies:</label>
                        <input type="number" id="friendly" min="1" max="20" value={friendlyCount} onChange={e => setFriendlyCount(e.target.value)} className="bg-gray-700 border border-gray-600 rounded p-2 w-20 text-center" disabled={!canStart}/>
                    </div>
                    <div className="flex items-center gap-2">
                        <label htmlFor="enemy" className="font-bold text-red-400">Enemies:</label>
                        <input type="number" id="enemy" min="1" max="20" value={enemyCount} onChange={e => setEnemyCount(e.target.value)} className="bg-gray-700 border border-gray-600 rounded p-2 w-20 text-center" disabled={!canStart}/>
                    </div>
                    <button onClick={handleStart} disabled={!canStart} className="bg-green-600 hover:bg-green-500 px-4 py-2 rounded disabled:opacity-50">Start</button>
                </div>
                <div className="flex items-center gap-2">
                    <button onClick={onPause} disabled={!isRunning} className="bg-yellow-600 hover:bg-yellow-500 px-4 py-2 rounded disabled:opacity-50">Pause</button>
                    <button onClick={onResume} disabled={!isPaused} className="bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded disabled:opacity-50">Resume</button>
                    <button onClick={onReset} disabled={isIdle} className="bg-red-600 hover:bg-red-500 px-4 py-2 rounded disabled:opacity-50">Reset</button>
                </div>
            </div>
            <div className="flex items-center justify-between border-t border-gray-700 pt-4">
                 <div className="flex items-center gap-2">
                    <span className="font-bold">AI Level:</span>
                    <button onClick={() => setAiLevel('basic')} className="bg-gray-600 hover:bg-gray-500 px-3 py-1 rounded">Basic</button>
                    <button onClick={() => setAiLevel('normal')} className="bg-gray-600 hover:bg-gray-500 px-3 py-1 rounded">Normal</button>
                    <button onClick={() => setAiLevel('advanced')} className="bg-gray-600 hover:bg-gray-500 px-3 py-1 rounded">Advanced</button>
                </div>
                <div className="flex items-center gap-2">
                    <span className="font-bold">Speed:</span>
                    <button onClick={() => setSpeed(0.5)} className="bg-gray-600 hover:bg-gray-500 px-3 py-1 rounded">0.5x</button>
                    <button onClick={() => setSpeed(1)} className="bg-gray-600 hover:bg-gray-500 px-3 py-1 rounded">1x</button>
                    <button onClick={() => setSpeed(2)} className="bg-gray-600 hover:bg-gray-500 px-3 py-1 rounded">2x</button>
                </div>
            </div>
        </div>
    );
};

export default ControlPanel;