import React from 'react';
import '../styles/InteractiveSection.css';
import MNIST from './MNIST';


const InteractiveSection = ({type,title}) => {
  return (
    <div className="interactive-section">
      <h2>Model Playground</h2>
      {type === 'mnist' && <MNIST/>}
      {type === 'resnset'}
    </div>
  );
};

export default InteractiveSection;
