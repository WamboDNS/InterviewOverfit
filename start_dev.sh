#!/bin/bash
set -e

echo "🎮 Starting InterviewOverfit Development Environment"
echo "=================================================="

# Colors for better output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ Error: Please run this script from the project root directory${NC}"
    exit 1
fi

# Check for required tools
echo -e "${BLUE}🔍 Checking required tools...${NC}"

# Check for uv
if ! command -v uv &> /dev/null; then
    echo -e "${RED}❌ Error: 'uv' is not installed${NC}"
    echo -e "${YELLOW}   Please install uv: https://github.com/astral-sh/uv${NC}"
    echo -e "${YELLOW}   Or run: curl -LsSf https://astral.sh/uv/install.sh | sh${NC}"
    exit 1
fi
echo -e "${GREEN}✅ uv found: $(uv --version)${NC}"

# Check for pnpm
if ! command -v pnpm &> /dev/null; then
    echo -e "${RED}❌ Error: 'pnpm' is not installed${NC}"
    echo -e "${YELLOW}   Please install pnpm: https://pnpm.io/installation${NC}"
    echo -e "${YELLOW}   Or run: npm install -g pnpm${NC}"
    exit 1
fi
echo -e "${GREEN}✅ pnpm found: $(pnpm --version)${NC}"

# Check for Python 3.13+ (required by pyproject.toml)
if ! python3 --version | grep -E "Python 3\.(1[3-9]|[2-9][0-9])" > /dev/null; then
    echo -e "${YELLOW}⚠️  Warning: Python 3.13+ is recommended for this project${NC}"
    echo -e "${YELLOW}   Current version: $(python3 --version)${NC}"
else
    echo -e "${GREEN}✅ Python found: $(python3 --version)${NC}"
fi

# Check for required environment variable
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  Warning: ANTHROPIC_API_KEY environment variable not set${NC}"
    echo -e "${YELLOW}   The game will prompt for an API key when you start playing${NC}"
    echo ""
else
    echo -e "${GREEN}✅ ANTHROPIC_API_KEY is set${NC}"
fi

# Install backend dependencies using uv
echo -e "${BLUE}📦 Installing backend dependencies with uv...${NC}"
cd back-end

# Create virtual environment and install dependencies
if [ ! -f ".venv/pyvenv.cfg" ]; then
    echo -e "${BLUE}   Creating virtual environment...${NC}"
    uv venv
fi

echo -e "${BLUE}   Installing Python packages...${NC}"
uv pip install -e . --quiet

echo -e "${GREEN}✅ Backend dependencies installed${NC}"

# Install frontend dependencies using pnpm
echo -e "${BLUE}📦 Installing frontend dependencies with pnpm...${NC}"
cd ../frontend

# Check if node_modules exists and is up to date
if [ ! -d "node_modules" ] || [ "package.json" -nt "node_modules/.pnpm" ]; then
    echo -e "${BLUE}   Installing Node.js packages...${NC}"
    pnpm install --silent
else
    echo -e "${GREEN}   Frontend dependencies are up to date${NC}"
fi

echo -e "${GREEN}✅ Frontend dependencies installed${NC}"

# Function to cleanup background processes
cleanup() {
    echo -e "\n${YELLOW}🛑 Stopping servers...${NC}"
    # Kill all background jobs
    jobs -p | xargs -r kill 2>/dev/null || true
    # Also kill any processes on our ports
    lsof -ti:8000 | xargs -r kill 2>/dev/null || true
    lsof -ti:5173 | xargs -r kill 2>/dev/null || true
    echo -e "${GREEN}✅ All servers stopped${NC}"
    exit 0
}
trap cleanup INT TERM EXIT

# Start backend server in background
echo -e "${BLUE}🚀 Starting FastAPI backend server...${NC}"
cd ../back-end

# Use uv to run the app in the virtual environment
uv run python app.py > backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
echo -e "${YELLOW}⏳ Waiting for backend to start...${NC}"
for i in {1..10}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Backend server is running at http://localhost:8000${NC}"
        echo -e "${BLUE}📚 API docs available at http://localhost:8000/docs${NC}"
        break
    fi
    if [ $i -eq 10 ]; then
        echo -e "${RED}❌ Backend server failed to start after 10 seconds${NC}"
        echo -e "${YELLOW}   Check backend.log for errors:${NC}"
        tail -n 20 backend.log
        exit 1
    fi
    sleep 1
done

# Start frontend development server
echo -e "${BLUE}🚀 Starting React frontend development server...${NC}"
cd ../frontend

# Use pnpm to start the dev server
pnpm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait for frontend to start
echo -e "${YELLOW}⏳ Waiting for frontend to start...${NC}"
for i in {1..15}; do
    if curl -s http://localhost:5173 > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Frontend server is running at http://localhost:5173${NC}"
        break
    fi
    if [ $i -eq 15 ]; then
        echo -e "${YELLOW}⚠️  Frontend might still be starting (this can take a while)${NC}"
        echo -e "${YELLOW}   Check frontend.log for details or try refreshing the browser${NC}"
        break
    fi
    sleep 1
done

echo ""
echo -e "${GREEN}🎉 Development environment is ready!${NC}"
echo -e "${BLUE}📱 Frontend: ${NC}http://localhost:5173"
echo -e "${BLUE}🖥️  Backend:  ${NC}http://localhost:8000"
echo -e "${BLUE}📖 API Docs: ${NC}http://localhost:8000/docs"
echo -e "${BLUE}🏥 Health:   ${NC}http://localhost:8000/health"
echo ""
echo -e "${GREEN}🎮 To play the game:${NC}"
echo "1. Open http://localhost:5173 in your browser"
echo "2. Select your role (SDE)" 
echo "3. Choose a level to start the Boss Battle"
echo "4. Enter your Anthropic API key when prompted"
echo ""
echo -e "${YELLOW}📋 Available commands:${NC}"
echo -e "${BLUE}   Backend logs:${NC}  tail -f back-end/backend.log"
echo -e "${BLUE}   Frontend logs:${NC} tail -f frontend/frontend.log" 
echo -e "${BLUE}   Test API:${NC}      curl http://localhost:8000/api/info"
echo ""
echo -e "${RED}🛑 Press Ctrl+C to stop all servers${NC}"

# Keep script running and wait for user interrupt
while true; do
    # Check if servers are still running
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo -e "${RED}❌ Backend server stopped unexpectedly${NC}"
        echo -e "${YELLOW}   Check backend.log for errors:${NC}"
        tail -n 10 back-end/backend.log
        exit 1
    fi
    
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo -e "${YELLOW}⚠️  Frontend server stopped${NC}"
        echo -e "${YELLOW}   Check frontend.log for details:${NC}"
        tail -n 10 frontend/frontend.log
    fi
    
    sleep 5
done
