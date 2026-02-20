# MediRoute AI 🏥

An intelligent medical evacuation chatbot that helps users find the nearest appropriate hospital based on their symptoms, location, and insurance.

## 🎯 Features

- **Intelligent Routing**: AI-powered hospital matching based on symptoms, location, and insurance
- **Modern UI**: Beautiful gradient-accented chat interface with glass-morphism effects
- **Real-time Chat**: Interactive conversation with typing indicators
- **Multi-Agent System**: Orchestrated agent workflow for optimal decision making

## 🏗️ Architecture

### Backend (FastAPI + LangGraph)
- **Framework**: FastAPI with async support
- **AI**: Multi-agent system using LangGraph
- **Agents**: Intake, Match, Orchestrator, and Response agents
- **Location**: `app/` directory

### Frontend (React + Vite)
- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS with custom gradients
- **API Client**: Axios
- **Location**: `frontend/` directory

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API key (or other LLM provider)

### Manual Start

**Backend:**
```bash
# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
# In a new terminal
cd frontend

# Install dependencies
npm install

# Start the frontend
npm run dev
```

### Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🎨 UI/UX Features

- **Gradient Accents**: Blue-to-purple gradient theme throughout
- **Glass Effects**: Modern glass-morphism for cards and containers
- **Loading States**: Animated typing indicator with "MediRoute AI is thinking..."
- **Smooth Animations**: Fade-in animations for messages
- **Responsive Design**: Works on desktop and mobile devices
- **Auto-scroll**: Messages automatically scroll to the latest

## 📁 Project Structure

```
mediroute_ai/
├── app/                          # Backend application
│   ├── agents/                   # LangGraph agent system
│   │   ├── nodes/               # Agent node implementations
│   │   ├── prompts/             # Agent prompts
│   │   └── tools/               # Agent tools
│   ├── data/                    # Hospital data
│   ├── models/                  # Pydantic models
│   ├── routers/                 # API routes
│   ├── services/                # Business logic
│   └── main.py                  # FastAPI entry point
├── frontend/                     # Frontend application
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── ChatContainer.jsx
│   │   │   ├── ChatMessage.jsx
│   │   │   ├── ChatInput.jsx
│   │   │   └── TypingIndicator.jsx
│   │   ├── App.jsx
│   │   └── index.css            # Tailwind CSS
│   └── package.json
└── start_dev.sh                 # Development start script

```

## 🔧 Configuration

### Backend CORS
The backend is configured to accept requests from `http://localhost:5173` (Vite default port).
Update in `app/main.py` if needed.

### Frontend Proxy
The frontend proxies `/chat` requests to `http://localhost:8000`.
Update in `frontend/vite.config.js` if needed.

## 💬 Usage Example

Simply describe your situation in the chat:

> "I have chest pain and I'm in downtown Los Angeles. I have Blue Cross insurance."

The AI will:
1. Extract your symptoms, location, and insurance
2. Match you with appropriate hospitals
3. Provide recommendations with distances and details

## 🛠️ Development

### Building for Production

**Frontend:**
```bash
cd frontend
npm run build
```

The production files will be in `frontend/dist/`.

### Running Tests
```bash
# Backend tests (if configured)
pytest

# Frontend tests (if configured)
cd frontend
npm test
```

## 📝 License

See LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.