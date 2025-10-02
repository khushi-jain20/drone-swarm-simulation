// frontend/src/components/Asset.js
import React from 'react';
import assetImg from '../assets/ground_asset.png';

const Asset = ({ asset, worldDimensions }) => {
    // --- THE FIX: Increased the size of the asset from 60 to 80px ---
    // You can adjust this value further if you like. 80 is a good starting point.
    const assetSize = 100; // Was 60
    // -----------------------------------------------------------------
    
    const isDestroyed = asset.health <= 0;

    const style = {
        position: 'absolute',
        width: `${assetSize}px`,
        height: `${assetSize}px`,
        left: `calc(${(asset.position.x / worldDimensions.width) * 100}% - ${assetSize / 2}px)`,
        top: `calc(${(asset.position.y / worldDimensions.height) * 100}% - ${assetSize / 2}px)`,
        filter: isDestroyed ? 'grayscale(100%) brightness(50%)' : 'none',
        transition: 'filter 0.5s',
    };

    return <img src={assetImg} alt="Ground Asset" style={style} />;
};

export default Asset;
