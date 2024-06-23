// src/components/DrawingPad.js
import React, { useRef, useState, useEffect } from 'react';

const MNIST = () => {
    const canvasRef = useRef(null);
    const contextRef = useRef(null);
    const [isDrawing, setIsDrawing] = useState(false);

    useEffect(() => {
        const canvas = canvasRef.current;
        canvas.width = 280;
        canvas.height = 280;
        canvas.style.width = `${280}px`;
        canvas.style.height = `${280}px`;

        const context = canvas.getContext('2d');
        context.scale(1, 1);
        context.lineCap = 'round';
        context.strokeStyle = 'black';
        context.lineWidth = 10;
        contextRef.current = context;
    }, []);

    const startDrawing = ({ nativeEvent }) => {
        const { offsetX, offsetY } = nativeEvent;
        contextRef.current.beginPath();
        contextRef.current.moveTo(offsetX, offsetY);
        setIsDrawing(true);
    };

    const finishDrawing = () => {
        contextRef.current.closePath();
        setIsDrawing(false);
    };

    const draw = ({ nativeEvent }) => {
        if (!isDrawing) return;
        const { offsetX, offsetY } = nativeEvent;
        contextRef.current.lineTo(offsetX, offsetY);
        contextRef.current.stroke();
    };

    const clearCanvas = () => {
        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');
        context.clearRect(0, 0, canvas.width, canvas.height);
    };

    const saveCanvas = () => {
        const canvas = canvasRef.current;
        const dataUrl = canvas.toDataURL('image/png');
        // Send dataUrl to the backend for inference
    };

    return (
        <div>
            <canvas
                ref={canvasRef}
                onMouseDown={startDrawing}
                onMouseUp={finishDrawing}
                onMouseMove={draw}
                onMouseLeave={finishDrawing}
            />
            <button onClick={clearCanvas}>Clear</button>
            <button onClick={saveCanvas}>Save</button>
        </div>
    );
};

export default MNIST;
