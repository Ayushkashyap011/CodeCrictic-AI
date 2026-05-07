import React from 'react';
import { useNavigate } from 'react-router-dom';
import './ProblemCard.css';

function ProblemCard({ problem }) {
  const navigate = useNavigate();

  const getDifficultyClass = (difficulty) => {
    switch (difficulty.toLowerCase()) {
      case 'easy':
        return 'difficulty-easy';
      case 'medium':
        return 'difficulty-medium';
      case 'hard':
        return 'difficulty-hard';
      default:
        return '';
    }
  };

  const handleClick = () => {
    const problemId = problem?.id || problem?._id;
    if (problemId) {
      console.log('Navigating to problem:', problemId);
      navigate(`/workspace/${problemId}`);
    } else {
      console.error('Problem ID is missing:', problem);
    }
  };

  if (!problem) {
    return <div className="problem-card">Problem data not available</div>;
  }

  return (
    <div className="problem-card" onClick={handleClick}>
      <div className="problem-card-header">
        <h3 className="problem-title">{problem.title}</h3>
        <span className={`difficulty-badge ${getDifficultyClass(problem.difficulty)}`}>
          {problem.difficulty}
        </span>
      </div>
      
      <p className="problem-description">
        {problem.description ? problem.description.substring(0, 120) + '...' : 'No description available'}
      </p>
      
      <div className="problem-card-footer">
        <div className="problem-tags">
          {problem.category && <span className="category-tag">{problem.category}</span>}
          {problem.tags && problem.tags.slice(0, 2).map((tag, idx) => (
            <span key={idx} className="tag">{tag}</span>
          ))}
        </div>
        <div className="problem-acceptance">
          <span className="acceptance-label">Acceptance:</span>
          <span className="acceptance-rate">{problem.acceptance_rate || 'N/A'}</span>
        </div>
      </div>
    </div>
  );
}

export default ProblemCard;
