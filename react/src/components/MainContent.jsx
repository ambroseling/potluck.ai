// src/components/MainContent.js
import React from 'react';
import Card from './Card'; // Assuming Card component is located in src/components/Card.js

const MainContent = () => {
    const mainContentStyle = {
        padding: '20px',
        maxWidth: '800px',
        margin: '0 auto'
    };

    const titleStyle = {
        fontSize: '2.5rem',
        fontWeight: 'bold',
        marginBottom: '10px'
    };

    const descriptionStyle = {
        fontSize: '1.2rem',
        marginBottom: '20px'
    };

    const buttonContainerStyle = {
        marginBottom: '20px'
    };

    const buttonStyle = {
        marginRight: '10px',
        padding: '10px 20px',
        backgroundColor: '#007bff',
        color: '#fff',
        border: 'none',
        borderRadius: '5px',
        textDecoration: 'none',
        fontSize: '1rem'
    };

    const posts = [
        {
            id: 1,
            title: 'Post 1',
            description: 'Description of Post 1',
            imageUrl: 'https://placeimg.com/300/200/tech'
        },
        {
            id: 2,
            title: 'Post 2',
            description: 'Description of Post 2',
            imageUrl: 'https://placeimg.com/300/200/nature'
        },
        {
            id: 3,
            title: 'Post 3',
            description: 'Description of Post 3',
            imageUrl: 'https://placeimg.com/300/200/architecture'
        },
        // Add more posts as needed
    ];

    return (
        <div style={mainContentStyle}>
            <h1 style={titleStyle}>Main Title</h1>
            <p style={descriptionStyle}>Description about your content goes here.</p>

            <div style={buttonContainerStyle}>
                <a href="#" style={buttonStyle}>Button 1</a>
                <a href="#" style={buttonStyle}>Button 2</a>
                <a href="#" style={buttonStyle}>Button 3</a>
                <a href="#" style={buttonStyle}>Button 4</a>
            </div>

            <div>
                {posts.map(post => (
                    <Card key={post.id} post={post} />
                ))}
            </div>
        </div>
    );
};

export default MainContent;
