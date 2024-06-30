// src/pages/PostDetail.js
import React from 'react';
import { useParams } from 'react-router-dom';
import BlogSection from './BlogSection';
import InteractiveSection from './InteractiveSection';
import '../styles/PostDetail.css';

const PostDetail = ({ posts }) => {
    const { id } = useParams();
    const post = posts.find(post => post.id === parseInt(id));

    if (!post) {
        return <div>Post not found</div>;
    }

    return (
        <div className="post-detail">
            <div className="section interactive-section">
                <InteractiveSection type={post.type}/>
            </div>
            <div className="section blog-section">
                <BlogSection post={post} />
            </div>
        </div>
    );
};

export default PostDetail;
