import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHeart } from '@fortawesome/free-solid-svg-icons';
import { useNavigate } from 'react-router-dom';
import '../styles/Card.css';

const Card = ({ post }) => {
    const navigate = useNavigate();

    const handleLearnMore = () => {
        navigate(`/post/${post.id}`);
    };
    return (
        <div className="card">
            <div className="card-content">
                <div className="content-left">
                    <img src={post.imageUrl} alt={post.title} className="image-thumbnail" />
                </div>
                <div className="content-right">
                    <div className="like-button">
                        <button className="btn-like">
                            <FontAwesomeIcon icon={faHeart} />  
                        </button>
                    </div>
                    <h2>{post.title}</h2>
                    <p>{post.description}</p>
                    <div className="button-group">
                        <button className="btn" onClick={handleLearnMore}>Learn More</button>
                        <button className="btn">Try it Out!</button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Card;
