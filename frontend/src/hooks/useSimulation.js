// frontend/src/hooks/useSimulation.js
import { useState, useEffect, useCallback } from 'react';

const wsClient = {
    instance: null,
};

const SIMULATION_WEBSOCKET_URL = "ws://localhost:8000/simulation";

export const useSimulation = () => {
    const [isConnected, setIsConnected] = useState(false);
    const [data, setData] = useState(null);

    const sendCommand = (command, payload = {}) => {
        if (wsClient.instance && wsClient.instance.readyState === WebSocket.OPEN) {
            wsClient.instance.send(JSON.stringify({ command, ...payload }));
        } else {
            console.error("Cannot send command: WebSocket is not open.");
        }
    };

    const connect = useCallback(() => {
        if (wsClient.instance && wsClient.instance.readyState !== WebSocket.CLOSED) {
            return;
        }

        const ws = new WebSocket(SIMULATION_WEBSOCKET_URL);
        wsClient.instance = ws;

        ws.onopen = () => {
            console.log("WebSocket Connection Established.");
            setIsConnected(true);
        };

        ws.onmessage = (event) => {
            const receivedData = JSON.parse(event.data);
            setData(receivedData);
        };

        ws.onerror = (error) => {
            console.error("WebSocket Error:", error);
        };

        ws.onclose = () => {
            console.log("WebSocket Disconnected.");
            setIsConnected(false);
            wsClient.instance = null;
            setTimeout(() => {
                console.log("Attempting to reconnect...");
                connect();
            }, 3000);
        };
    }, []);

    useEffect(() => {
        connect();
        return () => {
            if (wsClient.instance) {
                // Do not auto-close in development for a better experience
            }
        };
    }, [connect]);

    const startGame = (payload) => sendCommand('start', payload);
    const pauseGame = () => sendCommand('pause');
    const resumeGame = () => sendCommand('resume');

    // --- THE FIX: The resetGame function is now much simpler ---
    // It no longer manually sets the data to null.
    // It just tells the backend to reset, and the backend's response will naturally update the UI.
    const resetGame = () => {
        sendCommand('reset');
    };
    // -----------------------------------------------------------

    return { data, isConnected, startGame, pauseGame, resumeGame, resetGame };
};