// src/pages/PostDetail.js
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

const PostDetail = () => {
    const { id } = useParams();
    const [post, setPost] = useState(null);
    const [input, setInput] = useState('');
    const [result, setResult] = useState(null);

    useEffect(() => {
        // Fetch the post by id from an API or a local file
        fetch(`/api/posts/${id}`)
            .then(response => response.json())
            .then(data => setPost(data));
    }, [id]);

    const handleInference = () => {
        // Call your inference API with the input
        fetch('/api/inference', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ input }),
        })
            .then(response => response.json())
            .then(data => setResult(data));
    };

    if (!post) return <p>Loading...</p>;

    return (
        <div className="post-detail">
            <div className="text-section">
                <h1>{post.title}</h1>
                <p>{post.content}</p>
            </div>
            <div className="model-section">
                <h2>Model Inference</h2>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Enter input for inference"
                />
                <button onClick={handleInference}>Run Inference</button>
                {result && <p>Result: {result}</p>}
            </div>
        </div>
    );
};

export default PostDetail;
