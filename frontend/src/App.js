import React, { useState, useEffect } from 'react';
import { useSimulation } from './hooks/useSimulation';

import ControlPanel from './components/ControlPanel';
import SimulationScreen from './components/SimulationScreen';
import MetricsPanel from './components/MetricsPanel';
import EventLog from './components/EventLog';
import AnalysisPanel from './components/AnalysisPanel';
import CommunicationPanel from './components/CommunicationPanel';

function App() {
    const [worldDimensions, setWorldDimensions] = useState(null);
    const { data, isConnected, startGame, pauseGame, resumeGame, resetGame } = useSimulation();

    useEffect(() => {
        const fetchWorldConfig = async () => {
            try {
                const response = await fetch('http://localhost:8000/config/world');
                const config = await response.json();
                setWorldDimensions({
                    width: config.world_width,
                    height: config.world_height
                });
            } catch (error) {
                console.error("Failed to fetch world configuration:", error);
            }
        };
        fetchWorldConfig();
    }, []);

    if (!isConnected || !data?.simulation_state || !worldDimensions) {
        return (
            <div className="bg-gray-900 text-white h-screen flex items-center justify-center font-mono">
                <h1 className="text-2xl animate-pulse">
                    {isConnected ? "Awaiting Simulation Data..." : "Connecting to Server..."}
                </h1>
            </div>
        );
    }

    return (
        <div className="bg-gray-900 text-gray-200 h-screen font-mono flex flex-col p-4 gap-4">
            {/* --- UPDATED HEADER SECTION --- */}
            <header className="flex items-center justify-between flex-shrink-0">
                {/* Empty div for balancing the layout and centering the title */}
                <div className="w-1/5"></div>

                {/* Centered Title and new Tagline */}
                <div className="text-center">
                    <h1 className="text-4xl text-amber-400 font-bold font-orbitron">VAJRA</h1>
                    <p className="text-sm text-gray-400 tracking-wider font-sans">Swift. Decisive. Secure.</p>
                </div>

                {/* Connection status moved to the top-right corner */}
                <div className="w-1/5 text-right">
                    <p>Connection: <span className={isConnected ? 'text-green-500' : 'text-red-500'}>{isConnected ? 'Connected' : 'Disconnected'}</span></p>
                </div>
            </header>
            {/* --- END OF UPDATED HEADER --- */}

            <main className="flex-grow flex gap-4 overflow-hidden">
                {/* Left Column */}
                <div className="w-1/5 flex flex-col gap-4">
                    <AnalysisPanel analysisData={data.analysis} />
                    <CommunicationPanel logs={data.event_log} />
                </div>

                {/* Center Column */}
                <div className="flex-grow flex flex-col gap-4 w-3/5">
                    <ControlPanel
                        status={data.simulation_state.status}
                        onStart={startGame} onPause={pauseGame} onResume={resumeGame} onReset={resetGame}
                    />
                    <div className="flex-grow relative border-2 border-gray-700 rounded-lg">
                        <SimulationScreen
                            drones={data.drones}
                            assets={data.assets}
                            visualEvents={data.visual_events}
                            worldDimensions={worldDimensions}
                        />
                    </div>
                </div>

                {/* Right Column */}
                <div className="w-1/5 flex flex-col gap-4">
                    <EventLog logs={data.event_log} />
                    <MetricsPanel metrics={data.metrics} />
                </div>
            </main>
        </div>
    );
}

export default App;