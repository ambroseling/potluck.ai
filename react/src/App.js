import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import MainContent from './components/MainContent';
import PostDetail from './components/PostDetail';
import './App.css';

const App = () => {
  const posts = [
    {
        id: 1,
        title: 'MNIST Digit Classification Inference',
        description: 'One of the most famous image classification problems in deep learning. We let you explore how to provide your own hand drawn input and run inference on our model.',
        imageUrl: 'https://i.ibb.co/nbHh1Wv/mnist.png'
    },
    {
        id: 2,
        title: 'Open-SORA: Video Generation Inference',
        description: 'Explore generative modelling with SORA, specifically video generation with providing a prompt. Understand how it works under the hood and run the model yourself.',
        imageUrl: 'https://i.ibb.co/b13fsBs/Gemini-Generated-Image-f66fr5f66fr5f66f.jpg'
    },
    {
        id: 3,
        title: 'Recommendation Systems',
        description: 'We dive into how recommendation systems work, how they run in production and how they serve you with such low latency.',
        imageUrl: 'https://i.ibb.co/RQXns7P/recommendation.png'
    },
    {
      id: 4,
      title: 'Stable Diffusion',
      description: 'We bring image geneartion closer to you. Showing you the inner theory of a diffusion model and how it generates images to your liking.',
      imageUrl: 'https://i.ibb.co/x6nHB50/Stability-AI-Stable-Diffusion-Art.jpg'
  }
  ,
  {
    id: 5,
    title: 'Quantization',
    description: 'Run a model that was quantized to see the difference in performance, learn about how quantizaton helps you save memory.',
    imageUrl: 'https://i.ibb.co/R0f79pD/220px-2-bit-resolution-analog-comparison.png'
},
    // Add more posts as needed
];


    return (
        <Router>
            <Header />
            <main>
                <Routes>
                    <Route path="/" element={<MainContent posts={posts}/>} />
                    <Route path="/post/:id" element={<PostDetail posts={posts} />} />
                </Routes>
              
            </main>
            <Footer />
        </Router>
    );
};

export default App;
