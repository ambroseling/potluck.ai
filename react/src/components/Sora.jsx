import React, { useState, useRef, useEffect } from 'react';
import '../styles/Sora.css';  // Make sure to import the CSS file
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperclip, faArrowUp } from '@fortawesome/free-solid-svg-icons';
const Sora = () => {
    const samplers = ["PNDM","DDIM","DDPM"]
    const [prompt, setPrompt] = useState("");
    const [samplingSteps, setSamplingSteps] = useState(50); // Default value for sampling steps
    const [selectedSampler, setSelectedSampler] = useState(samplers[0]);
    const videoRef = useRef(null);
    const [videoSrc, setVideoSrc] = useState("");
    const [socket, setSocket] = useState(null);
    const [status, setStatus] = useState("");
    const [message, setMessage] = useState("");

    // Effect to update video source when videoSrc changes
    useEffect(() => {
        if (videoRef.current && videoSrc) {
            // Assign videoSrc to the video element
            videoRef.current.src = videoSrc;
        }
    }, [videoSrc]);

    useEffect(() => {
        // Establish WebSocket connection
        const ws = new WebSocket('ws://localhost:8000/ws');

        ws.onopen = () => {
            console.log('WebSocket connected');
            setSocket(ws);
        };

        ws.onmessage = (event) => {
            setStatus(`Received response: ${event.data}`);

            const data = JSON.parse(event.data);
            console.log(data);
            if (data.video) {
                const decodedVideo = atob(data.video);
                const byteNumbers = new Array(decodedVideo.length);
                for (let i = 0; i < decodedVideo.length; i++) {
                    byteNumbers[i] = decodedVideo.charCodeAt(i);
                }
                const byteArray = new Uint8Array(byteNumbers);
                console.log(byteArray);
                const blob = new Blob([byteArray], { type: 'video/mp4' });
                console.log(URL.createObjectURL(blob));
                setVideoSrc(URL.createObjectURL(blob));
            }
            else {
                console.error("Received invalid data format");
                setStatus("Received invalid data format");
            }
        };
        ws.onerror = (error) => {
            console.error("WebSocket error:", error);
        };

        ws.onclose = () => {
            console.log("WebSocket closed");
        };

        return () => {
            if (ws) {
                ws.close();
            }
        };
    }, []);

    const handlePromptChange = (event) => {
        setPrompt(event.target.value);
    };

    const handleSamplingStepsChange = (event) => {
        setSamplingSteps(event.target.value);
    };

    const handleSamplerChange = (event) => {
        setSelectedSampler(event.target.value);
    };

    const handleSendPrompt = () => {
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({
                config: "sora",
                prompt: prompt,
                sampling_steps: samplingSteps,
                sampler: selectedSampler
            }));
        }
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'flex-start' }}>
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <video ref={videoRef} width="512" height="512" controls>
                </video>
                <div className="prompt-bar">
                    <i className="icon-attachment"></i>
                    <input 
                        type="text" 
                        value={prompt} 
                        onChange={handlePromptChange} 
                        placeholder="Prompt OpenSora" 
                        className="prompt-input" 
                    />
                    <button onClick={handleSendPrompt} className="send-button">
                        <FontAwesomeIcon icon={faArrowUp} />
                    </button>
                </div>
            </div>
            <div style={{ flex: 0.3, display: 'flex', flexDirection: 'column', marginLeft: '20px' }}>
                <h3>Settings</h3>
                <label>
                    Sampling Steps:
                    <input 
                        type="number" 
                        value={samplingSteps} 
                        onChange={handleSamplingStepsChange} 
                        style={{ marginTop: '10px', padding: '5px', width: '100%' }} 
                    />
                </label>
                <label style={{ marginTop: '20px' }}>
                    Sampler:
                    <select 
                        value={selectedSampler} 
                        onChange={handleSamplerChange} 
                        style={{ marginTop: '10px', padding: '5px', width: '100%' }}>
                        {samplers.map(sampler => (
                            <option key={sampler} value={sampler}>{sampler}</option>
                        ))}
                    </select>
                </label>
            </div>
        </div>
    );
};

export default Sora;
