// src/components/Card.js
import React from 'react';
import '../styles/Card.css';
const Card = ({ post }) => {
    return (
        <div className="card">
            <div className="card-image">
                <img src={post.imageUrl} alt={post.title} />
            </div>
            <div className="card-content">
                <h2>{post.title}</h2>
                <p>{post.description}</p>
                <div className="button-group">
                    <button className="btn">Button 1</button>
                    <button className="btn">Button 2</button>
                </div>
                <div className="like-button">
                    <button className="btn-like">Like</button>
                </div>
            </div>
        </div>
    );
};

export default Card;
