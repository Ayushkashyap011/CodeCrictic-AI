import React, { useState, useEffect } from 'react';
import ProblemCard from '../components/ProblemCard';
import LoadingSpinner from '../components/LoadingSpinner';
import api from '../api/axios';
import './ProblemList.css';

function ProblemList() {
  const [problems, setProblems] = useState([]);
  const [filteredProblems, setFilteredProblems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [difficulty, setDifficulty] = useState('All');
  const [category, setCategory] = useState('All');
  const [searchTerm, setSearchTerm] = useState('');
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    fetchProblems();
  }, []);

  useEffect(() => {
    filterProblems();
  }, [problems, difficulty, category, searchTerm]);

  const fetchProblems = async () => {
    try {
      setLoading(true);
      const response = await api.get('/api/v1/problems/');
      setProblems(response.data);
      
      // Extract unique categories
      const uniqueCategories = [...new Set(response.data.map(p => p.category))].sort();
      setCategories(uniqueCategories);
      
      setError(null);
    } catch (err) {
      setError('Failed to fetch problems. Please try again later.');
      console.error('Error fetching problems:', err);
    } finally {
      setLoading(false);
    }
  };

  const filterProblems = () => {
    let filtered = problems;

    // Filter by difficulty
    if (difficulty !== 'All') {
      filtered = filtered.filter(p => p.difficulty === difficulty);
    }

    // Filter by category
    if (category !== 'All') {
      filtered = filtered.filter(p => p.category === category);
    }

    // Filter by search term
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(p =>
        p.title.toLowerCase().includes(term) ||
        p.description.toLowerCase().includes(term)
      );
    }

    setFilteredProblems(filtered);
  };

  return (
    <div className="problem-list-container">
      <div className="problem-list-header">
        <h1>Coding Problems</h1>
        <p className="problem-count">{filteredProblems.length} problems</p>
      </div>

      {error && (
        <div className="error-message">
          {error}
          <button onClick={fetchProblems} className="btn btn-secondary">Retry</button>
        </div>
      )}

      <div className="filter-section">
        <div className="filter-group">
          <label htmlFor="difficulty">Difficulty</label>
          <select
            id="difficulty"
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
            className="filter-select"
          >
            <option>All</option>
            <option>Easy</option>
            <option>Medium</option>
            <option>Hard</option>
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="category">Category</label>
          <select
            id="category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="filter-select"
          >
            <option>All</option>
            {categories.map(cat => (
              <option key={cat}>{cat}</option>
            ))}
          </select>
        </div>

        <div className="filter-group search-group">
          <label htmlFor="search">Search</label>
          <input
            id="search"
            type="text"
            placeholder="Search by title or description..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>
      </div>

      {loading ? (
        <LoadingSpinner />
      ) : filteredProblems.length === 0 ? (
        <div className="no-problems">
          <p>No problems found matching your criteria.</p>
          <button
            onClick={() => {
              setDifficulty('All');
              setCategory('All');
              setSearchTerm('');
            }}
            className="btn btn-primary"
          >
            Reset Filters
          </button>
        </div>
      ) : (
        <div className="problems-grid">
          {filteredProblems.map((problem, idx) => (
            <ProblemCard key={problem.id || problem._id || `problem-${idx}`} problem={problem} />
          ))}
        </div>
      )}
    </div>
  );
}

export default ProblemList;
