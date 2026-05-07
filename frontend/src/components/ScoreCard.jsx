import React, { useEffect, useState } from 'react';
import './ScoreCard.css';

function ScoreCard({ label, score }) {
  const [fill, setFill] = useState(0);

  useEffect(() => {
    const timer = setTimeout(() => {
      setFill(score * 10);
    }, 100);
    return () => clearTimeout(timer);
  }, [score]);

  const getScoreColor = (score) => {
    if (score >= 8) return '#00b894';
    if (score >= 5) return '#fdcb6e';
    return '#e17055';
  };

  return (
    <div className="score-card">
      <div className="score-header">
        <span className="score-label">{label}</span>
        <span className="score-value">{score}/10</span>
      </div>
      <div className="score-bar">
        <div
          className="score-bar-fill"
          style={{
            width: `${fill}%`,
            backgroundColor: getScoreColor(score),
          }}
        />
      </div>
    </div>
  );
}

export default ScoreCard;
