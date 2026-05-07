import React from 'react';
import './TestCaseResult.css';

function TestCaseResult({ result }) {
  return (
    <div className="test-case-result">
      <div className="test-case-header">
        <div className="test-case-number">
          <span className="test-number">Test {result.test_number}</span>
          {result.passed ? (
            <span className="test-status-pass">✓ Passed</span>
          ) : (
            <span className="test-status-fail">✗ Failed</span>
          )}
        </div>
      </div>

      <div className="test-case-content">
        <div className="test-case-section">
          <span className="section-label">Input:</span>
          <pre className="code-block">{result.input || 'N/A'}</pre>
        </div>

        <div className="test-case-section">
          <span className="section-label">Expected Output:</span>
          <pre className="code-block">{result.expected || 'N/A'}</pre>
        </div>

        <div className="test-case-section">
          <span className="section-label">Actual Output:</span>
          <pre className={`code-block ${result.passed ? 'success' : 'error'}`}>
            {result.actual || 'N/A'}
          </pre>
        </div>

        {result.error && (
          <div className="test-case-section">
            <span className="section-label error">Error:</span>
            <pre className="code-block error-block">{result.error}</pre>
          </div>
        )}

        {result.runtime_ms && (
          <div className="test-case-meta">
            <span className="meta-item">
              <strong>Runtime:</strong> {result.runtime_ms}ms
            </span>
            {result.memory_kb && (
              <span className="meta-item">
                <strong>Memory:</strong> {result.memory_kb}KB
              </span>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default TestCaseResult;
