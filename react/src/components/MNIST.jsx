import React, { useRef, useState, useEffect } from 'react';
import '../styles/MNIST.css'; // Import the CSS file

const MNIST = () => {
    const canvasRef = useRef(null);
    const contextRef = useRef(null);
    const [isDrawing, setIsDrawing] = useState(false);
    const [socket, setSocket] = useState(null);
    const [status, setStatus] = useState("");
    useEffect(() => {
        // WebSocket setup
        const ws = new WebSocket('ws://localhost:8000/ws');  // Replace with your WebSocket endpoint
        ws.onopen = () => {
            console.log('WebSocket connected');
            setSocket(ws);
        };

        ws.onmessage = (event) => {
            setStatus(`Received response: ${event.data}`);
            // Handle received data as needed
        };

        ws.onclose = () => {
            console.log('WebSocket closed');
            setSocket(null);
        };

        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        // Cleanup function for WebSocket
        return () => {
            if (ws) {
                ws.close();
            }
        };
    },[]);  // Empty dependency array ensures this runs only once on component mount


    useEffect(() => {
        // Canvas setup
        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');
        canvas.width = 280;
        canvas.height = 280;
        canvas.style.width = `${280}px`;
        canvas.style.height = `${280}px`;

        context.scale(1, 1);
        context.lineCap = 'round';
        context.strokeStyle = 'black';
        context.lineWidth = 10;
       // Set contextRef to the canvas context
       contextRef.current = context;
    },[]);
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

    const saveCanvas = async () => {
        const canvas = canvasRef.current;
        const dataUrl = canvas.toDataURL('image/png');
        const textData = "mnist"; // Replace with actual text data
        console.log(dataUrl);
        const payload = {
            text: textData,
            image: dataUrl,
        };
    
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify(payload));  // Convert payload to JSON string
            setStatus('Sending text and image...');
        } else {
            console.error('WebSocket connection not established.');
        }
    };

    return (
        <div className="col-container">
            <canvas
                ref={canvasRef}
                onMouseDown={startDrawing}
                onMouseUp={finishDrawing}
                onMouseMove={draw}
                onMouseLeave={finishDrawing}
                className="drawing-canvas"
            />
            <div className="row-container">
            <button className="button" onClick={clearCanvas}>Clear</button>
            <button className="button" onClick={saveCanvas}>Save</button>

            </div>
        </div>
    );
};

export default MNIST;
