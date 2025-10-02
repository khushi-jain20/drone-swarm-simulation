// src/components/Tracer.js
import React from 'react';
import projectileImg from '../assets/projectile.png';

const Tracer = ({ event, worldDimensions }) => {
    const filterStyle = event.team === 'friendly' 
        ? 'hue-rotate(180deg) saturate(2) brightness(1.5)' 
        : 'hue-rotate(0deg) saturate(3) brightness(1.2)';

    const startX = (event.position.x / worldDimensions.width) * 100;
    const startY = (event.position.y / worldDimensions.height) * 100;
    
    const dx = event.target_position.x - event.position.x;
    const dy = event.target_position.y - event.position.y;
    
    const distance = Math.sqrt(dx*dx + dy*dy);
    const angleRad = Math.atan2(dy, dx);
    const angleDeg = angleRad * (180 / Math.PI);

    const style = {
        position: 'absolute',
        left: `${startX}%`,
        top: `${startY}%`,
        
        // --- THE FIX: Make the beam thinner and shorter ---
        height: '3px', // Thinner beam (was 4px)
        width: `${distance * 0.4}px`, // BEAM IS NOW 40% OF THE TOTAL DISTANCE (was 100%)
        // ---------------------------------------------------
        
        transformOrigin: 'left center',
        transform: `rotate(${angleDeg}deg)`,
        filter: filterStyle,
        animation: `fadeout ${event.ttl}s linear forwards`
    };

    return <img src={projectileImg} alt="Projectile" style={style} />;
};

export default Tracer;