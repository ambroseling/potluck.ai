import React from 'react';

const LoadingComponent = ({message,progress}) => {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <div className="loading-bar" style={{ width: '100%', height: '20px', backgroundColor: '#ccc', borderRadius: '5px', overflow: 'hidden' }}>
                <div style={{ width: `${progress}%`, height: '100%', backgroundColor: '#76c7c0' }}></div>
            </div>
            <p>{message == "" ? "Enter a prompt and see what Sora can generate!": message}</p>
            <style>
                {`
                    @keyframes loading {
                        0% { width: 0; }
                        100% { width: 100%; }
                    }
                `}
            </style>
        </div>
    );
};

export default LoadingComponent;
