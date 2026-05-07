# CodeCritic AI - LeetCode Clone with AI Code Review

A complete coding practice platform that combines LeetCode-style problems with AI-powered code reviews powered by Groq.

---

## Tech Stack

**Backend:**
- Python 3.11
- FastAPI (API framework)
- Uvicorn (ASGI server)
- MongoDB Atlas (database)
- Motor (async MongoDB driver)
- Groq API (AI code reviews)

**Frontend:**
- React 18
- React Router v6
- Monaco Editor (code editor)
- Axios (HTTP client)
- CSS custom properties (theming)

**Infrastructure:**
- Local code execution (Python, JavaScript, Java, C++)
- Event loop policy: Windows Proactor Event Loop
- 15-second execution timeout per test case
- Concurrent test execution with semaphore (limit: 4)

---

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a `.env` file with your configuration:
   ```env
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?appName=codecritic
   DATABASE_NAME=codecritic
   GROQ_API_KEY=gsk_your_groq_api_key_here
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Seed the database with 12 problems:
   ```bash
   python seed_problems.py --drop
   ```

5. Start the server:
   ```bash
   python run.py
   ```
   
   The backend will run on **http://127.0.0.1:8000**

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```
   
   The frontend will run on **http://localhost:3000**

---

## API Endpoints

| Endpoint | Method | Description | Request | Response |
|----------|--------|-------------|---------|----------|
| `/api/v1/problems` | GET | Fetch all problems | - | List of problems |
| `/api/v1/problems/{id}` | GET | Fetch single problem | - | Problem object |
| `/api/v1/execute/run` | POST | Test code on examples | `{ problem_id, code, language }` | Test results for 3 examples |
| `/api/v1/execute/submit` | POST | Test code on hidden cases | `{ problem_id, code, language }` | Test results for 5 hidden + submission_id |
| `/api/v1/ai/review/{submission_id}` | GET | Poll AI review status | - | AI review with scores and feedback |

---

## Getting API Keys

### MongoDB Atlas

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a cluster (free tier available)
3. Create a database user with password
4. Get connection string: `mongodb+srv://user:password@cluster.mongodb.net/?appName=codecritic`
5. Create a database named `codecritic`

### Groq API

1. Go to [Groq Console](https://console.groq.com)
2. Sign up for free account
3. Go to API Keys section
4. Generate a new API key
5. Copy and paste into your `.env` file

---

## Features

✅ **12 Fully Configured Problems**
- Two Sum, Valid Parentheses, Reverse Linked List, Maximum Subarray
- Best Time to Buy and Sell Stock, Climbing Stairs, Binary Search
- Longest Common Prefix, Number of Islands, Merge Intervals
- Coin Change, Word Search

✅ **Two-Phase Testing**
- **Run Code**: Test against 3 public example test cases (instant feedback)
- **Submit**: Test against 5 hidden test cases + AI code review

✅ **Automatic I/O Handling**
- Users submit only the Solution class
- Backend automatically parses input and calls the solution method
- Problem-specific parsing logic for different input formats

✅ **Local Code Execution**
- Supports Python, JavaScript, Java, C++
- 15-second execution timeout
- Handles compilation errors, runtime errors, timeout errors
- Concurrent test execution for performance

✅ **AI-Powered Code Review**
- Groq API integration (llama-3.1-8b-instant)
- Real-time scoring: Correctness, Optimization, Readability, Interview Readiness
- Detailed feedback: Strengths, Issues, Improvements
- Complexity analysis: Time & Space complexity
- Interview tips and estimated developer level

✅ **Professional UI/UX**
- Dark/Light theme toggle with persistence
- Monaco Editor with syntax highlighting
- Responsive design for all screen sizes
- Toast notifications for user feedback
- Loading states and visual feedback

---

## Usage Workflow

### 1. View Problems
- Navigate to `/problems` to see all 12 problems
- Filter by difficulty (Easy, Medium, Hard)
- Click on a problem to open the workspace

### 2. Run Code
- Select a language from the dropdown
- Write your solution (submit only the Solution class)
- Click "Run Code" to test against examples
- See test results with actual output vs expected

### 3. Submit Code
- When ready, click "Submit"
- Code is tested against 5 hidden test cases
- Wait for AI review (typically 2-3 seconds)
- See detailed AI feedback with scores

### 4. AI Review Panel
- View score breakdown: Correctness, Optimization, etc.
- Read strengths and potential issues
- See improvement suggestions
- Learn complexity analysis and interview tips

---

## Problem Structure

Each problem includes:

```json
{
  "id": "problem_id",
  "title": "Problem Title",
  "slug": "problem-slug",
  "difficulty": "Easy|Medium|Hard",
  "description": "Problem description...",
  "constraints": ["Constraint 1", "Constraint 2", ...],
  "examples": [
    {
      "input": "executable format",
      "output": "expected output",
      "explanation": "human-readable explanation"
    }
  ],
  "hidden_testcases": [
    { "input": "...", "output": "..." }
  ],
  "starter_code": {
    "python": "class Solution:\n...",
    "javascript": "class Solution { ... }",
    "java": "public class Solution { ... }",
    "cpp": "class Solution { ... };"
  }
}
```

---

## Key Implementation Details

### Code Wrapper Pattern
- User submits: `class Solution: def coinChange(self, coins, amount): ...`
- Backend wraps with: Input parsing → Solution instantiation → Method call → Output capture
- Eliminates need for users to write boilerplate I/O code

### Local Code Execution
- Replaces rate-limited Piston API
- Subprocess execution with 15-second timeout
- Windows-compatible with Proactor event loop policy
- Concurrent execution with semaphore control

### AI Review Polling
- Frontend polls `/api/v1/ai/review/{submission_id}` every 3 seconds
- Maximum 10 attempts (30 seconds total)
- Smooth scroll to review panel when ready
- Error handling for timeout scenarios

### Language Sync
- When language is changed, editor loads problem's starter code for that language
- Fallback to default STARTER_CODE if not available
- On problem load, defaults to Python

---

## File Structure

```
CodeCritic-AI/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── execute.py (execution endpoints)
│   │   │   └── ai_review.py (AI review endpoint)
│   │   ├── services/
│   │   │   ├── piston.py (local executor)
│   │   │   ├── code_wrapper.py (I/O parsing)
│   │   │   └── groq_client.py (AI API)
│   │   ├── models/
│   │   │   ├── submission.py (request/response schemas)
│   │   │   └── problem.py (problem schema)
│   │   └── main.py (FastAPI app)
│   ├── data/
│   │   └── problems.json (12 problems)
│   ├── run.py (server startup)
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── ProblemList.jsx
│   │   │   ├── Workspace.jsx (editor & execution)
│   │   │   └── SubmissionResult.jsx
│   │   ├── components/
│   │   │   ├── Toast.jsx (notifications)
│   │   │   ├── TestCaseResult.jsx
│   │   │   ├── ScoreCard.jsx
│   │   │   └── LoadingSpinner.jsx
│   │   └── App.jsx
│   └── package.json
│
└── CHANGES_SUMMARY.md (full documentation)
```

---

## Common Issues & Solutions

**Issue: Backend fails to start on Windows**
- Solution: Event loop policy is set to Proactor in `run.py` before uvicorn config

**Issue: Piston API returns 401 Unauthorized**
- Solution: Using local subprocess executor instead of public Piston API

**Issue: Code execution returns "N/A"**
- Solution: All result processing moved inside async context block where result is defined

**Issue: Language dropdown doesn't change starter code**
- Solution: `handleLanguageChange` now loads from `problem.starter_code` or STARTER_CODE fallback

---

## Performance Metrics

- Code Execution: ~100-300ms per test case
- AI Review: ~2-3 seconds (Groq API response time)
- Database Operations: <100ms
- Frontend Render: <50ms

---

## Future Improvements

- [ ] Docker sandboxing for safer execution
- [ ] Extended language support (C#, Go, Rust, etc.)
- [ ] User authentication & submission history
- [ ] Leaderboards and achievements
- [ ] Custom test cases
- [ ] Problem discussions and hints
- [ ] Video tutorials and explanations
- [ ] IDE extensions/plugins

---

## 🔒 Security

**IMPORTANT**: A MongoDB credential leak was detected and removed from Git history. If you had this repository cloned before May 7, 2026:

### Immediate Actions Required:
1. **Rotate MongoDB credentials** in MongoDB Atlas console
2. **Reset Groq API key** if exposed
3. Pull the latest changes: `git pull --force`

### Protecting Your Credentials:
✅ **Never commit sensitive data** to Git
- `.env` files are listed in `.gitignore` (ignored automatically)
- Use environment variables instead
- Use `.env.example` as a template for other developers

### Best Practices:
- Keep `.env` in `.gitignore` ✓ (already configured)
- Use `config.py` with empty defaults and load from `.env` ✓ (already fixed)
- Rotate credentials regularly if exposed
- Use GitHub secret scanning alerts to catch issues early

---