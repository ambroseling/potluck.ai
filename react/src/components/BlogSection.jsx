import React from 'react';
import '../styles/BlogSection.css';

const BlogSection = () => {
  return (
    <div className="blog-section">
      <h2>Blog Section</h2>
      <div className="blog-content">
        <h3>Subtitle 1</h3>
        <p>This is some blog content. You can add images and equations here.</p>
        <img src="https://via.placeholder.com/150" alt="Placeholder" />
        {/* Example of an equation using MathJax or similar */}
        <p>Example equation: \( E = mc^2 \)</p>
        <h3>Subtitle 2</h3>
        <p>More blog content...</p>
      </div>
    </div>
  );
};

export default BlogSection;
