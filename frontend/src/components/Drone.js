// src/components/Drone.js
import React, { useState } from 'react';
import friendlyDroneImg from '../assets/friendly_drone.png';
import enemyDroneImg from '../assets/enemy_drone.png';

const Drone = ({ drone, worldDimensions }) => {
    const [imageError, setImageError] = useState(false);
    const imageSrc = drone.team === 'friendly' ? friendlyDroneImg : enemyDroneImg;
    const imageSize = 48;

    // --- We no longer need the rotation calculation ---
    // const isMoving = drone.velocity && (drone.velocity.x !== 0 || drone.velocity.y !== 0);
    // const rotationRad = isMoving ? Math.atan2(drone.velocity.y, drone.velocity.x) : 0;

    const containerStyle = {
        position: 'absolute',
        width: `${imageSize}px`,
        height: `${imageSize}px`,
        left: `calc(${(drone.position.x / worldDimensions.width) * 100}% - ${imageSize / 2}px)`,
        top: `calc(${(drone.position.y / worldDimensions.height) * 100}% - ${imageSize / 2}px)`,
        transition: 'left 0.05s linear, top 0.05s linear',
    };
    
    const imageStyle = {
        width: '100%',
        height: '100%',
        // --- THE FIX: The 'transform' and its 'transition' have been removed ---
    };

    const healthBarBackgroundStyle = {
        position: 'absolute',
        bottom: '-12px',
        left: '50%',
        transform: 'translateX(-50%)',
        width: '40px',
        height: '6px',
        backgroundColor: 'rgba(0, 0, 0, 0.7)',
        border: '1px solid #4B5563',
        borderRadius: '3px',
    };

    const healthBarForegroundStyle = {
        height: '100%',
        width: `${drone.health}%`,
        backgroundColor: drone.team === 'friendly' ? '#22C55E' : '#F97316',
        borderRadius: '2px',
        transition: 'width 0.2s ease-out',
    };


    return (
        <div style={containerStyle}>
            {imageError ? (
                <div style={{...imageStyle, backgroundColor: drone.team === 'friendly' ? 'cyan' : '#ff3838', border: '2px solid white'}} />
            ) : (
                <img 
                    src={imageSrc} 
                    alt={drone.team} 
                    style={imageStyle} 
                    onError={() => setImageError(true)}
                />
            )}
            <div style={healthBarBackgroundStyle}>
                <div style={healthBarForegroundStyle}></div>
            </div>
        </div>
    );
};

export default Drone;