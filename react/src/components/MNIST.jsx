import React, { useRef, useState, useEffect } from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import '../styles/MNIST.css'; // Import the CSS file

// Register the necessary components with Chart.js
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const MNIST = () => {
    const canvasRef = useRef(null);
    const contextRef = useRef(null);
    const [isDrawing, setIsDrawing] = useState(false);
    const [socket, setSocket] = useState(null);
    const [status, setStatus] = useState("");
    const [probabilities, setProbabilities] = useState(Array(10).fill(0));
    const [message, setMessage] = useState("");

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
            const data = JSON.parse(event.data);
            if (data.probabilities && Array.isArray(data.probabilities) && data.message) {
                setProbabilities(data.probabilities);
                setMessage(data.message);
            } 
            else if (data.messaage){
                setMessage(data.message);
            }
            else {
                console.error("Received invalid data format");
                setStatus("Received invalid data format");
            }
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
        }
        else {
            console.error('WebSocket connection not established.');
        }
    };

    const data = {
        labels: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
        datasets: [
            {
                label: 'Probability',
                data: probabilities,
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
            },
        ],
    };

    const options = {
        scales: {
            y: {
                beginAtZero: true,
            },
        },
    };

    return (
        <div className='row-container'>

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
        <div className='col-container'>
                <Bar data={data} options={options} />
                <p>{message}</p>  {/* Display the received message */}
        </div>
        </div>
    );
};

export default MNIST;
