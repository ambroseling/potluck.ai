import React from 'react';
import '../styles/InteractiveSection.css';
import MNIST from './MNIST';
import Sora from './Sora';

const InteractiveSection = ({type,title}) => {
  return (
    <div className="interactive-section">
      <h2>Playground</h2>
      {type === 'mnist' && <MNIST/>}
      {type === 'sora' && <Sora/>}
    </div>
  );
};

export default InteractiveSection;
