import React from 'react';
import './overview.css';

const Dialog = ({
  source_name,
  source_color,
  target_name,
  target_color,
  message,
}) => {
  const sourceStyle = { color: source_color };
  const targetStyle = { color: target_color };
  const borderStyle = { borderColor: source_color };
  
  if (source_name === target_name) {
    return (
      <div className="custom-action-box" style={borderStyle}>
        <span style={sourceStyle}>{source_name}</span><br/>
        {message}
      </div>
    )
  }
  else {
    return (
      <div className="custom-message-box" style={borderStyle}>
        <span style={sourceStyle}>{source_name}</span> to{' '}
        <span style={targetStyle}>{target_name}</span>: <br />{message}
      </div>
    );
  }
};

export default Dialog;