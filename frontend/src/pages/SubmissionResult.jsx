import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ScoreCard from '../components/ScoreCard';
import TestCaseResult from '../components/TestCaseResult';
import LoadingSpinner from '../components/LoadingSpinner';
import api from '../api/axios';
import './SubmissionResult.css';

function SubmissionResult() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [submission, setSubmission] = useState(null);
  const [aiReview, setAiReview] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSubmissionAndReview();
  }, [id]);

  const fetchSubmissionAndReview = async () => {
    try {
      setLoading(true);
      // Note: You'd need an endpoint to get submission by ID
      // For now, we'll just try to get the AI review
      try {
        const reviewResponse = await api.get(`/api/v1/ai/review/${id}`);
        setAiReview(reviewResponse.data);
      } catch (err) {
        console.error('Error fetching review:', err);
      }
      setError(null);
    } catch (err) {
      setError('Failed to load submission details.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <div className="error-container">
        <p>{error}</p>
        <button onClick={() => navigate('/problems')} className="btn btn-primary">
          Back to Problems
        </button>
      </div>
    );
  }

  if (!aiReview) {
    return (
      <div className="error-container">
        <p>Submission not found.</p>
        <button onClick={() => navigate('/problems')} className="btn btn-primary">
          Back to Problems
        </button>
      </div>
    );
  }

  return (
    <div className="submission-result-container">
      <button onClick={() => navigate('/problems')} className="back-button">
        ← Back to Problems
      </button>

      <div className="submission-header">
        <h1>Submission Result</h1>
        <span className={`status-badge ${aiReview.status === 'success' ? 'success' : 'fallback'}`}>
          {aiReview.status === 'success' ? '✓ Accepted' : '⚠ Review Generated'}
        </span>
      </div>

      {/* AI Review Dashboard */}
      <div className="review-dashboard">
        <div className="dashboard-section">
          <h2>AI Code Review</h2>

          {/* Scores */}
          <div className="scores-section">
            <div className="scores-grid">
              <ScoreCard
                label="Correctness"
                score={aiReview.scores?.correctness || 5}
              />
              <ScoreCard
                label="Optimization"
                score={aiReview.scores?.optimization || 5}
              />
              <ScoreCard
                label="Readability"
                score={aiReview.scores?.readability || 5}
              />
              <ScoreCard
                label="Interview Readiness"
                score={aiReview.scores?.interview_readiness || 5}
              />
              <ScoreCard
                label="Senior Engineer"
                score={aiReview.scores?.senior_engineer || 5}
              />
            </div>
          </div>

          {/* Level and Summary */}
          <div className="summary-section">
            <div className="level-container">
              <span className="level-badge">
                {aiReview.estimated_level || 'Junior Developer'}
              </span>
            </div>
            <p className="summary-text">{aiReview.summary}</p>
          </div>

          {/* Strengths, Issues, Improvements */}
          <div className="review-cards">
            {aiReview.strengths && aiReview.strengths.length > 0 && (
              <div className="review-card strengths">
                <h3>✓ Strengths</h3>
                <ul>
                  {aiReview.strengths.map((strength, idx) => (
                    <li key={idx}>{strength}</li>
                  ))}
                </ul>
              </div>
            )}

            {aiReview.issues && aiReview.issues.length > 0 && (
              <div className="review-card issues">
                <h3>⚠ Issues</h3>
                <ul>
                  {aiReview.issues.map((issue, idx) => (
                    <li key={idx}>{issue}</li>
                  ))}
                </ul>
              </div>
            )}

            {aiReview.improvements && aiReview.improvements.length > 0 && (
              <div className="review-card improvements">
                <h3>💡 Improvements</h3>
                <ul>
                  {aiReview.improvements.map((improvement, idx) => (
                    <li key={idx}>{improvement}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Complexity */}
          {aiReview.complexity && (
            <div className="complexity-section">
              <h3>Time & Space Complexity</h3>
              <div className="complexity-grid">
                {aiReview.complexity.time_complexity && (
                  <div className="complexity-card">
                    <span className="complexity-label">Time Complexity</span>
                    <span className="complexity-value">
                      {aiReview.complexity.time_complexity}
                    </span>
                    <p className="complexity-explanation">
                      {aiReview.complexity.time_explanation}
                    </p>
                  </div>
                )}
                {aiReview.complexity.space_complexity && (
                  <div className="complexity-card">
                    <span className="complexity-label">Space Complexity</span>
                    <span className="complexity-value">
                      {aiReview.complexity.space_complexity}
                    </span>
                    <p className="complexity-explanation">
                      {aiReview.complexity.space_explanation}
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Optimized Approach */}
          {aiReview.optimized_approach && (
            <div className="optimized-section">
              <h3>Optimized Approach</h3>
              <div className="code-block">
                <pre>{aiReview.optimized_approach}</pre>
              </div>
            </div>
          )}

          {/* Interview Tips */}
          {aiReview.interview_tips && aiReview.interview_tips.length > 0 && (
            <div className="tips-section">
              <h3>🎯 Interview Tips</h3>
              <ul className="tips-list">
                {aiReview.interview_tips.map((tip, idx) => (
                  <li key={idx}>{tip}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      <div className="submission-actions">
        <button onClick={() => navigate('/problems')} className="btn btn-primary">
          Solve Another Problem
        </button>
      </div>
    </div>
  );
}

export default SubmissionResult;
