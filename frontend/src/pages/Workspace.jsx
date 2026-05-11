import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Editor from '@monaco-editor/react';
import LoadingSpinner from '../components/LoadingSpinner';
import ScoreCard from '../components/ScoreCard';
import TestCaseResult from '../components/TestCaseResult';
import Toast from '../components/Toast';
import api from '../api/axios';
import './Workspace.css';

const STARTER_CODE = {
  python: `from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        pass
`,
  javascript: `class Solution {
    twoSum(nums, target) {
        
    }
}
`,
  java: `class Solution {
    public int[] twoSum(int[] nums, int target) {
        
    }
}
`,
  cpp: `class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        
    }
};
`,
};

function Workspace() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [problem, setProblem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Code execution state
  const [code, setCode] = useState(STARTER_CODE.python);
  const [language, setLanguage] = useState('python');
  const [stdin, setStdin] = useState('');
  const [runLoading, setRunLoading] = useState(false);
  const [submitLoading, setSubmitLoading] = useState(false);

  // Results state
  const [activeTab, setActiveTab] = useState('console');
  const [consoleOutput, setConsoleOutput] = useState('');
  const [consoleError, setConsoleError] = useState('');
  const [testResults, setTestResults] = useState([]);
  const [submissionStatus, setSubmissionStatus] = useState(null);
  const [submissionId, setSubmissionId] = useState(null);

  // AI Review state
  const [aiReview, setAiReview] = useState(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiReviewError, setAiReviewError] = useState(null);
  const [pollAttempts, setPollAttempts] = useState(0);
  const aiReviewRef = useRef(null);
  const pollIntervalRef = useRef(null);

  // Submission History state
  const [submissionHistory, setSubmissionHistory] = useState([]);
  const [expandedSubmission, setExpandedSubmission] = useState(null);

  // Toast state
  const [toast, setToast] = useState(null);

  useEffect(() => {
    console.log('Workspace mount - id:', id);
    if (id) {
      fetchProblem();
    } else {
      setError('Problem ID not found. Please select a problem from the list.');
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
      }
    };
  }, []);

  const fetchProblem = async () => {
    try {
      setLoading(true);
      console.log('Fetching problem with id:', id);
      const response = await api.get(`/api/v1/problems/${id}`);
      console.log('Problem fetched:', response.data);
      setProblem(response.data);
      const problemLanguage = response.data.languages?.[0] || 'python';
      setLanguage(problemLanguage);
      setCode(response.data.starter_code?.[problemLanguage] || STARTER_CODE[problemLanguage] || '');
      setError(null);
    } catch (err) {
      console.error('Error fetching problem:', err.response?.data || err.message);
      setError('Failed to load problem. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleLanguageChange = (newLanguage) => {
    setLanguage(newLanguage);
    if (problem?.starter_code?.[newLanguage]) {
      setCode(problem.starter_code[newLanguage]);
    } else {
      setCode(STARTER_CODE[newLanguage] || '');
    }
  };

  const handleRunCode = async () => {
    if (!id) {
      setAiReviewError('Problem ID not found');
      return;
    }
    try {
      setRunLoading(true);
      setConsoleOutput('');
      setConsoleError('');
      setTestResults([]);

      const response = await api.post('/api/v1/execute/run', {
        problem_id: id,
        code,
        language,
      });

      // Run code returns test results for examples
      setTestResults(response.data.test_results || []);
      setSubmissionStatus(response.data.status);
      setActiveTab('test-results');
    } catch (err) {
      const errMsg = err.response?.data?.detail || err.response?.data?.message || 'Error running code';
      setConsoleError(errMsg);
      setToast({ message: errMsg, type: 'error' });
      setActiveTab('console');
    } finally {
      setRunLoading(false);
    }
  };

  const handleSubmitCode = async () => {
    if (!id) {
      setAiReviewError('Problem ID not found');
      return;
    }
    try {
      setSubmitLoading(true);
      setConsoleOutput('');
      setConsoleError('');
      setAiReview(null);
      setAiLoading(false);
      setAiReviewError(null);
      setPollAttempts(0);

      const response = await api.post('/api/v1/execute/submit', {
        problem_id: id,
        code,
        language,
      });

      setTestResults(response.data.test_results || []);
      setSubmissionStatus(response.data.status);
      setSubmissionId(response.data.submission_id);
      setActiveTab('test-results');

      // Start polling for AI review
      if (response.data.submission_id) {
        setAiLoading(true);
        startPollingReview(response.data.submission_id);
      }
    } catch (err) {
      const errMsg = err.response?.data?.message || 'Error submitting code';
      setConsoleError(errMsg);
      setToast({ message: errMsg, type: 'error' });
      setActiveTab('console');
    } finally {
      setSubmitLoading(false);
    }
  };

  const startPollingReview = (subId) => {
    let attempts = 0;
    const maxAttempts = 10;

    if (pollIntervalRef.current) {
      clearInterval(pollIntervalRef.current);
    }

    pollIntervalRef.current = setInterval(async () => {
      attempts++;
      setPollAttempts(attempts);

      try {
        const response = await api.get(`/api/v1/ai/review/${subId}`);
        if (response.data && response.data.submission_id) {
          setAiReview(response.data);
          setAiLoading(false);
          setAiReviewError(null);
          clearInterval(pollIntervalRef.current);
          // Scroll to review section
          setTimeout(() => {
            aiReviewRef.current?.scrollIntoView({ behavior: 'smooth' });
          }, 300);
        }
      } catch (err) {
        console.error('Error polling review:', err);
      }

      if (attempts >= maxAttempts) {
        setAiLoading(false);
        setAiReviewError('AI review timed out. Please try again later.');
        clearInterval(pollIntervalRef.current);
      }
    }, 3000);
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

  if (!problem) {
    return <div className="error-container"><p>Problem not found</p></div>;
  }

  return (
    <div className="workspace">
      <div className="workspace-container">
        {/* Left Panel - Problem */}
        <div className="problem-panel">
          <div className="problem-header">
            <h1 className="problem-title">{problem.title}</h1>
            <span className={`difficulty-badge difficulty-${problem.difficulty.toLowerCase()}`}>
              {problem.difficulty}
            </span>
          </div>

          <div className="problem-section">
            <h3>Description</h3>
            <p className="problem-description">{problem.description}</p>
          </div>

          {problem.constraints && (
            <div className="problem-section">
              <h3>Constraints</h3>
              <ul className="constraints-list">
                {problem.constraints.map((constraint, idx) => (
                  <li key={idx}>{constraint}</li>
                ))}
              </ul>
            </div>
          )}

          {problem.examples && (
            <div className="problem-section">
              <h3>Examples</h3>
              <div className="examples-list">
                {problem.examples.map((example, idx) => (
                  <div key={idx} className="example">
                    <div className="example-item">
                      <span className="example-label">Input:</span>
                      <pre className="example-code">{example.input}</pre>
                    </div>
                    <div className="example-item">
                      <span className="example-label">Output:</span>
                      <pre className="example-code">{example.output}</pre>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Right Panel - Editor */}
        <div className="editor-panel">
          <div className="editor-header">
            <label htmlFor="language">Language</label>
            <select
              id="language"
              value={language}
              onChange={(e) => handleLanguageChange(e.target.value)}
              className="language-select"
            >
              <option value="python">Python</option>
              <option value="javascript">JavaScript</option>
              <option value="java">Java</option>
              <option value="cpp">C++</option>
            </select>
          </div>

          <div className="editor-wrapper">
            <Editor
              height="450px"
              language={language}
              value={code}
              onChange={(value) => setCode(value || '')}
              theme="vs-dark"
              options={{
                fontSize: 14,
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                automaticLayout: true,
                wordWrap: 'on',
              }}
            />
          </div>

          {language === 'python' && (
            <div className="stdin-section">
              <label htmlFor="stdin">Standard Input (Optional)</label>
              <textarea
                id="stdin"
                value={stdin}
                onChange={(e) => setStdin(e.target.value)}
                placeholder="Enter test input here..."
                className="stdin-input"
              />
            </div>
          )}

          <div className="editor-actions">
            <button
              onClick={handleRunCode}
              disabled={runLoading || submitLoading}
              className={`btn btn-secondary ${runLoading ? 'loading' : ''}`}
            >
              {runLoading ? '⟳ Running...' : '▶ Run Code'}
            </button>
            <button
              onClick={handleSubmitCode}
              disabled={runLoading || submitLoading}
              className={`btn btn-primary ${submitLoading ? 'loading' : ''}`}
            >
              {submitLoading ? '⟳ Submitting...' : '✓ Submit'}
            </button>
          </div>
        </div>
      </div>

      {/* Results Panel */}
      {(consoleOutput || consoleError || testResults.length > 0) && (
        <div className="results-panel">
          <div className="results-tabs">
            <button
              className={`tab-button ${activeTab === 'console' ? 'active' : ''}`}
              onClick={() => setActiveTab('console')}
            >
              Console
            </button>
            <button
              className={`tab-button ${activeTab === 'test-results' ? 'active' : ''}`}
              onClick={() => setActiveTab('test-results')}
            >
              Test Results {submissionStatus && `(${testResults.filter(t => t.passed).length}/${testResults.length})`}
            </button>
          </div>

          <div className="results-content">
            {activeTab === 'console' && (
              <div className="console-output">
                {consoleError && (
                  <div className="output-section error">
                    <h4>Error</h4>
                    <pre>{consoleError}</pre>
                  </div>
                )}
                {consoleOutput && (
                  <div className="output-section">
                    <h4>Output</h4>
                    <pre>{consoleOutput}</pre>
                  </div>
                )}
                {!consoleError && !consoleOutput && <p>No output</p>}
              </div>
            )}

            {activeTab === 'test-results' && testResults.length > 0 && (
              <div className="test-results-list">
                <div className="test-summary">
                  <span className={`summary-badge ${submissionStatus === 'Accepted' ? 'accepted' : 'rejected'}`}>
                    {submissionStatus}
                  </span>
                  <span className="summary-text">
                    {testResults.filter(t => t.passed).length}/{testResults.length} tests passed
                  </span>
                </div>
                {testResults.map((result) => (
                  <TestCaseResult key={result.test_number} result={result} />
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* AI Review Panel */}
      {(aiReview || aiLoading || aiReviewError) && (
        <div className="ai-review-section" ref={aiReviewRef}>
          <div className="ai-review-header">
            <h2>🤖 CodeCritic AI Review</h2>
            {aiLoading && <span className="loading-text">Analyzing your code...</span>}
          </div>

          {aiReviewError && (
            <div className="ai-error-message">
              {aiReviewError}
            </div>
          )}

          {aiLoading && (
            <div className="ai-loading-card">
              <p>🤖 CodeCritic AI is analyzing your code...</p>
              <div className="spinner"></div>
              <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '8px' }}>
                Attempt {pollAttempts} of 10
              </p>
            </div>
          )}

          {aiReview && (
            <div className="ai-review-content">
              {/* Scores */}
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
              </div>

              {/* Level and Summary */}
              <div className="review-summary">
                <span className="level-badge">
                  {aiReview.estimated_level || 'Junior Developer'}
                </span>
                <p className="summary-text">{aiReview.summary}</p>
              </div>

              {/* Strengths, Issues, Improvements */}
              <div className="review-sections">
                {aiReview.strengths && aiReview.strengths.length > 0 && (
                  <div className="review-section strengths">
                    <h4>✓ Strengths</h4>
                    <ul>
                      {aiReview.strengths.map((strength, idx) => (
                        <li key={idx}>{strength}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {aiReview.issues && aiReview.issues.length > 0 && (
                  <div className="review-section issues">
                    <h4>⚠ Issues</h4>
                    <ul>
                      {aiReview.issues.map((issue, idx) => (
                        <li key={idx}>{issue}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {aiReview.improvements && aiReview.improvements.length > 0 && (
                  <div className="review-section improvements">
                    <h4>💡 Improvements</h4>
                    <ul>
                      {aiReview.improvements.map((improvement, idx) => (
                        <li key={idx}>{improvement}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              {/* Complexity */}
              {(aiReview.complexity?.time_complexity || aiReview.complexity?.space_complexity) && (
                <div className="complexity-section">
                  {aiReview.complexity.time_complexity && (
                    <div className="complexity-item">
                      <span className="complexity-label">Time Complexity:</span>
                      <span className="complexity-value">{aiReview.complexity.time_complexity}</span>
                    </div>
                  )}
                  {aiReview.complexity.space_complexity && (
                    <div className="complexity-item">
                      <span className="complexity-label">Space Complexity:</span>
                      <span className="complexity-value">{aiReview.complexity.space_complexity}</span>
                    </div>
                  )}
                </div>
              )}

              {/* Interview Tips */}
              {aiReview.interview_tips && aiReview.interview_tips.length > 0 && (
                <div className="interview-tips">
                  <h4>🎯 Interview Tips</h4>
                  <ul>
                    {aiReview.interview_tips.map((tip, idx) => (
                      <li key={idx}>{tip}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Toast Notification */}
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
}

export default Workspace;
