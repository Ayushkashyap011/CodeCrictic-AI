import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

function Home() {
  const navigate = useNavigate();

  return (
    <div className="home">
      <div className="home-hero">
        <div className="hero-content">
          <h1 className="hero-title">
            Code<span className="gradient-text">Critic</span> AI
          </h1>
          <p className="hero-subtitle">
            Solve. Submit. Get AI-Powered Engineering Feedback.
          </p>
          
          <div className="hero-buttons">
            <button
              className="btn btn-primary btn-large"
              onClick={() => navigate('/problems')}
            >
              Start Solving
            </button>
            <button
              className="btn btn-secondary btn-large"
              onClick={() => navigate('/problems')}
            >
              View Problems
            </button>
          </div>
        </div>

        <div className="hero-background">
          <div className="gradient-orb orb-1"></div>
          <div className="gradient-orb orb-2"></div>
          <div className="gradient-orb orb-3"></div>
        </div>
      </div>

      <div className="features-section">
        <h2 className="section-title">Platform Features</h2>
        
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">🤖</div>
            <h3>AI Code Review</h3>
            <p>Get detailed feedback powered by Groq's advanced AI models. Understand your code quality instantly.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">✓</div>
            <h3>Real Test Cases</h3>
            <p>Submit your solution and run against comprehensive test cases with instant feedback on correctness.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Interview Readiness</h3>
            <p>Receive scores and tips to help you prepare for technical interviews and ace your next opportunity.</p>
          </div>
        </div>
      </div>

      <div className="cta-section">
        <h2>Ready to Improve Your Coding Skills?</h2>
        <p>Join hundreds of developers using CodeCritic AI to get better at problem-solving and coding interviews.</p>
        <button
          className="btn btn-primary btn-large"
          onClick={() => navigate('/problems')}
        >
          Get Started Now →
        </button>
      </div>
    </div>
  );
}

export default Home;
