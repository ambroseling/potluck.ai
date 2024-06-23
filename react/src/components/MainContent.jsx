import React from 'react';
import Card from './Card'; // Assuming Card component is located in src/components/Card.js
import '../styles/MainContent.css'; // Import your CSS file
import PostDetail from './PostDetail';
import { BrowserRouter as Router, Route } from 'react-router-dom';
const MainContent = ({posts}) => {

    return (
        <div className="main-content">
            <h1 className="main-title">Model Arena</h1>
            <p className="main-description">We let you run models on our gpus and help you learn about ML.</p>

            <div className="button-container">
                <a href="#" className="button">Button 1</a>
                <a href="#" className="button">Button 2</a>
                <a href="#" className="button">Button 3</a>
                <a href="#" className="button">Button 4</a>
            </div>

            <div style={{ marginTop: '60px' }}>
                {posts.map(post => (
                    <Card key={post.id} post={post} />
                ))}
            </div>
        </div>
    );
};

export default MainContent;
