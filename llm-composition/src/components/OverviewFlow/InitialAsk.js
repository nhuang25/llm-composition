import React from 'react';
import './overview.css';

const InitialAsk = ({ ask }) => {
  return (
    <div className="initial-ask-container">
      <p>{ask}</p>
    </div>
  );
};

export default InitialAsk;