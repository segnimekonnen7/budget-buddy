#!/usr/bin/env bash
set -euo pipefail

# ====== SETTINGS ======
API_PORT=5003
WEB_PORT=3000
PROJECT_DIR="internship-finder-deployed"

echo "🚀 Setting up Internship Finder (No Docker Version)"
echo "=================================================="

# ====== CHECK PREREQS ======
if ! command -v python3 >/dev/null 2>&1; then
  echo "❌ Python 3 is required. Please install Python 3.8+ and try again." >&2
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "❌ Node.js/npm is required. Please install from nodejs.org and try again." >&2
  exit 1
fi

echo "✅ Prerequisites check passed"

# ====== PREP PROJECT ======
echo "📁 Setting up project directory..."
rm -rf "$PROJECT_DIR"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Copy frontend
echo "📁 Copying frontend files..."
cp -r "../internship-finder" ./frontend

# Copy backend
echo "📁 Setting up backend..."
mkdir -p backend
cp "../simple-job-api.py" ./backend/app.py

# Create requirements.txt for backend
cat > backend/requirements.txt <<'REQ'
Flask==2.3.3
Flask-CORS==4.0.0
REQ

# ====== UPDATE FRONTEND TO USE API ======
echo "🔧 Updating frontend to use backend API..."

# Create API module
cat > frontend/src/api.ts <<'API'
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5003';

export interface Internship {
  id?: number;
  title: string;
  company: string;
  location: string;
  type: string;
  duration?: string;
  salary: string;
  description: string;
  category?: string;
  applyUrl?: string;
  source?: string;
}

export const api = {
  async searchInternships(keyword: string, location: string): Promise<Internship[]> {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/search`, {
        keyword,
        location,
        jobType: 'internship'
      });
      
      if (response.data.success) {
        return response.data.jobs.map((job: any, index: number) => ({
          id: index + 1,
          title: job.title,
          company: job.company,
          location: job.location,
          type: job.type,
          duration: '12 weeks',
          salary: job.salary,
          description: job.description,
          category: job.category,
          applyUrl: job.applyUrl,
          source: job.source
        }));
      }
      return [];
    } catch (error) {
      console.error('Error searching internships:', error);
      return [];
    }
  },

  async healthCheck(): Promise<boolean> {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/health`);
      return response.data.status === 'healthy';
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }
};
API

# Update App.tsx
cat > frontend/src/App.tsx <<'APP'
import { useState, useEffect } from 'react'
import { MagnifyingGlassIcon, BriefcaseIcon, MapPinIcon, CalendarIcon } from '@heroicons/react/24/outline'
import { api, type Internship } from './api'

function App() {
  const [searchTerm, setSearchTerm] = useState('')
  const [location, setLocation] = useState('')
  const [internships, setInternships] = useState<Internship[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [apiHealthy, setApiHealthy] = useState(false)

  useEffect(() => {
    const checkHealth = async () => {
      const healthy = await api.healthCheck()
      setApiHealthy(healthy)
      if (healthy) {
        handleSearch('software engineer', 'United States')
      }
    }
    checkHealth()
  }, [])

  const handleSearch = async (keyword: string, loc: string) => {
    if (!keyword.trim()) return
    
    setLoading(true)
    setError(null)
    
    try {
      const results = await api.searchInternships(keyword, loc)
      setInternships(results)
    } catch (err) {
      setError('Failed to search internships. Please try again.')
      console.error('Search error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleSearchSubmit = () => {
    handleSearch(searchTerm, location)
  }

  const filteredInternships = internships.filter(internship =>
    internship.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    internship.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
    internship.location.toLowerCase().includes(location.toLowerCase())
  )

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <BriefcaseIcon className="h-8 w-8 text-blue-600" />
              <h1 className="ml-2 text-2xl font-bold text-gray-900">Internship Finder</h1>
              <div className="ml-4 flex items-center">
                <div className={`w-2 h-2 rounded-full ${apiHealthy ? 'bg-green-500' : 'bg-red-500'}`}></div>
                <span className="ml-1 text-sm text-gray-600">
                  {apiHealthy ? 'API Connected' : 'API Disconnected'}
                </span>
              </div>
            </div>
            <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
              Post Internship
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Find Your Perfect Internship</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="relative">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search internships..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearchSubmit()}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div className="relative">
              <MapPinIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Location"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearchSubmit()}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <button 
              onClick={handleSearchSubmit}
              disabled={loading}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Searching...' : 'Search'}
            </button>
          </div>
          
          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800">{error}</p>
            </div>
          )}
        </div>

        <div className="space-y-4">
          {filteredInternships.map((internship) => (
            <div key={internship.id} className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="text-xl font-semibold text-gray-900">{internship.title}</h3>
                  <p className="text-lg text-blue-600 font-medium">{internship.company}</p>
                  <div className="flex items-center mt-2 space-x-4 text-sm text-gray-600">
                    <div className="flex items-center">
                      <MapPinIcon className="h-4 w-4 mr-1" />
                      {internship.location}
                    </div>
                    <div className="flex items-center">
                      <CalendarIcon className="h-4 w-4 mr-1" />
                      {internship.type}
                    </div>
                    {internship.duration && <span>{internship.duration}</span>}
                    <span className="text-green-600 font-medium">{internship.salary}</span>
                  </div>
                  <p className="mt-3 text-gray-700">{internship.description}</p>
                  {internship.source && (
                    <p className="mt-2 text-xs text-gray-500">Source: {internship.source}</p>
                  )}
                </div>
                <div className="ml-4 flex flex-col space-y-2">
                  {internship.applyUrl ? (
                    <a 
                      href={internship.applyUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-center"
                    >
                      Apply Now
                    </a>
                  ) : (
                    <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                      Apply Now
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredInternships.length === 0 && !loading && (
          <div className="text-center py-12">
            <BriefcaseIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No internships found</h3>
            <p className="text-gray-600">Try adjusting your search criteria</p>
          </div>
        )}

        {loading && (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Searching for internships...</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
APP

# Update Vite config for development
cat > frontend/vite.config.ts <<'VITE'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5003',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
VITE

# ====== INSTALL DEPENDENCIES ======
echo "📦 Installing backend dependencies..."
cd backend
python3 -m pip install -r requirements.txt

echo "📦 Installing frontend dependencies..."
cd ../frontend
npm install

# ====== START SERVICES ======
echo "🚀 Starting services..."

# Start backend in background
echo "Starting backend API on port ${API_PORT}..."
cd ../backend
python3 app.py &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 3

# Check if backend is running
if curl -s "http://localhost:${API_PORT}/api/health" | grep -q '"healthy"'; then
  echo "✅ Backend API is running"
else
  echo "❌ Backend failed to start"
  kill $BACKEND_PID 2>/dev/null || true
  exit 1
fi

# Start frontend
echo "Starting frontend on port ${WEB_PORT}..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Wait for frontend to start
echo "⏳ Waiting for frontend to start..."
sleep 5

echo ""
echo "🎉 Deployment complete!"
echo "=================================================="
echo ""
echo "📱 Access your application:"
echo "   Frontend: http://localhost:${WEB_PORT}"
echo "   Backend API: http://localhost:${API_PORT}"
echo ""
echo "🔧 Management commands:"
echo "   Stop backend: kill $BACKEND_PID"
echo "   Stop frontend: kill $FRONTEND_PID"
echo "   View backend logs: tail -f backend.log"
echo ""
echo "📊 API Endpoints:"
echo "   GET  http://localhost:${API_PORT}/api/health"
echo "   POST http://localhost:${API_PORT}/api/search"
echo "   GET  http://localhost:${API_PORT}/api/search?keyword=software&location=CA"
echo ""
echo "🌐 Your internship finder is now running!"
echo "   Open http://localhost:${WEB_PORT} in your browser"
echo ""

# Save PIDs for cleanup
echo "$BACKEND_PID" > backend.pid
echo "$FRONTEND_PID" > frontend.pid

echo "💡 To stop the services later, run:"
echo "   kill \$(cat backend.pid) \$(cat frontend.pid)"
echo "   rm backend.pid frontend.pid"
