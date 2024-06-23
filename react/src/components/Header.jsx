// src/components/Header.js
import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
    const headerStyle = {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '10px 300px', // Padding on top and bottom, and on left and right sides
        backgroundColor: 'rgb(245, 245, 245)', // Light gray background color
        color: '#000', // Black text color
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif'
    };

    const navStyle = {
        marginLeft: 'auto'  // Pushes the nav to the right
    };

    const logoStyle = {
        fontWeight: 'bold',
        fontSize: '1.5rem',
        color: '#000' // Black color for the logo text
    };

    return (
        <header style={headerStyle}>
            <div style={logoStyle}>
                2bros2gpus
            </div>
            <nav style={navStyle}>
                <ul style={{ listStyleType: 'none', margin: 0, padding: 0, display: 'flex' }}>
                    <li style={{ marginRight: '10px' }}><Link to="/" style={{ color: '#000', textDecoration: 'none' }}>Home</Link></li>
                    <li style={{ marginRight: '10px' }}><Link to="/about" style={{ color: '#000', textDecoration: 'none' }}>About</Link></li>
                    {/* Add more navigation links as needed */}
                </ul>
            </nav>
        </header>
    );
};

export default Header;
