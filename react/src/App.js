import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import MainContent from './components/MainContent';
import PostDetail from './components/PostDetail';
import './App.css';

const App = () => {
    return (
        <Router>
            <Header />
            <main>
                <Routes>
                    <Route path="/" element={<MainContent />} />
                    <Route path="/post/:id" element={<PostDetail />} />
                </Routes>
            </main>
            <Footer />
        </Router>
    );
};

export default App;
