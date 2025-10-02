// src/components/SimulationScreen.js
import React from 'react';
import Drone from './Drone';
import Asset from './Asset';
import Tracer from './Tracer';
import CommunicationLink from './CommunicationLink';

const SimulationScreen = ({ drones, assets, visualEvents, worldDimensions }) => {
    return (
        <div className="grid-background w-full h-full overflow-hidden">
            <div className="absolute top-2 left-2 text-white z-20 text-xs">
                <span>Drones: {drones?.length || 0}</span>
            </div>

            {assets?.map(asset => (
                <Asset key={asset.id} asset={asset} worldDimensions={worldDimensions} />
            ))}

            {drones?.map(drone => (
                <Drone key={drone.id} drone={drone} worldDimensions={worldDimensions} />
            ))}

            {visualEvents
                ?.filter(e => e.type === 'weapon_fire')
                .map(event => (
                    // --- FIX: Pass worldDimensions to the Tracer ---
                    <Tracer key={event.id} event={event} worldDimensions={worldDimensions} />
                ))}
            {visualEvents
                ?.filter(e => e.type === 'comm_link')
                .map(event => (
                    <CommunicationLink key={event.id} event={event} worldDimensions={worldDimensions} />
                ))}
            {/* --------------------- */}
        </div>
    );
};

export default SimulationScreen;
