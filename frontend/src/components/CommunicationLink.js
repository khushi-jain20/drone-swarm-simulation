// frontend/src/components/CommunicationLink.js
import React from 'react';

const CommunicationLink = ({ event, worldDimensions }) => {
    // Convert backend pixels to frontend percentages
    const startX = (event.position.x / worldDimensions.width) * 100;
    const startY = (event.position.y / worldDimensions.height) * 100;
    const endX = (event.target_position.x / worldDimensions.width) * 100;
    const endY = (event.target_position.y / worldDimensions.height) * 100;

    const style = {
        // Use a short fade-in/fade-out for a dynamic "blip" effect
        animation: `pulse ${event.ttl}s ease-in-out`,
    };

    return (
        <svg style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', zIndex: 0 }}>
            <line
                x1={`${startX}%`} y1={`${startY}%`}
                x2={`${endX}%`} y2={`${endY}%`}
                stroke="rgba(0, 255, 255, 0.4)" // Semi-transparent cyan
                strokeWidth="1.5"
                style={style}
            />
        </svg>
    );
};

export default CommunicationLink;