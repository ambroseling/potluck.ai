import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHeart } from '@fortawesome/free-solid-svg-icons';
import '../styles/Card.css';

const Card = ({ post }) => {
    return (
        <div className="card">
            <div className="card-content">
                <div className="content-left">
                    <img src={post.imageUrl} alt={post.title} className="image-thumbnail" />
                </div>
                <div className="content-right">
                    <h2>{post.title}</h2>
                    <p>{post.description}</p>
                    <div className="button-group">
                        <button className="btn">Button 1</button>
                        <button className="btn">Button 2</button>
                    </div>
                    <div className="like-button">
                        <button className="btn-like">
                            <FontAwesomeIcon icon={faHeart} /> Like
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Card;
