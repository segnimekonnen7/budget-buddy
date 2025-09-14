import { useState } from 'react'
import { MagnifyingGlassIcon, BuildingOfficeIcon, MapPinIcon, AcademicCapIcon } from '@heroicons/react/24/outline'

function App() {
  const [searchQuery, setSearchQuery] = useState('')
  const [location, setLocation] = useState('')
  const [selectedMajor, setSelectedMajor] = useState('')

  const majors = [
    'Computer Science',
    'Software Engineering', 
    'Information Technology',
    'Data Science',
    'Cybersecurity',
    'Computer Engineering',
    'Web Development',
    'Mobile Development'
  ]

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    console.log('Searching for:', { searchQuery, location, selectedMajor })
    // TODO: Implement search functionality
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <BuildingOfficeIcon className="h-8 w-8 text-indigo-600" />
              <h1 className="ml-3 text-2xl font-bold text-gray-900">
                🚀 Internship Finder
              </h1>
            </div>
            <div className="text-sm text-gray-500">
              Find your dream internship
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search Section */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Search Internships
          </h2>
          
          <form onSubmit={handleSearch} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Search Query */}
              <div>
                <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-2">
                  Keywords
                </label>
                <div className="relative">
                  <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <input
                    type="text"
                    id="search"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="e.g., software engineer, frontend, python"
                    className="pl-10 w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                  />
                </div>
              </div>

              {/* Location */}
              <div>
                <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-2">
                  Location
                </label>
                <div className="relative">
                  <MapPinIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <input
                    type="text"
                    id="location"
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    placeholder="e.g., San Francisco, Remote"
                    className="pl-10 w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                  />
                </div>
              </div>

              {/* Major */}
              <div>
                <label htmlFor="major" className="block text-sm font-medium text-gray-700 mb-2">
                  Major/Field
                </label>
                <div className="relative">
                  <AcademicCapIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <select
                    id="major"
                    value={selectedMajor}
                    onChange={(e) => setSelectedMajor(e.target.value)}
                    className="pl-10 w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                  >
                    <option value="">Select a major</option>
                    {majors.map((major) => (
                      <option key={major} value={major}>
                        {major}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            <button
              type="submit"
              className="w-full md:w-auto bg-indigo-600 text-white px-6 py-2 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors"
            >
              Search Internships
            </button>
          </form>
        </div>

        {/* Features Section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="text-3xl mb-4">🔍</div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Smart Search</h3>
            <p className="text-gray-600">
              Search across multiple job sources with intelligent filtering and ranking
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="text-3xl mb-4">🧠</div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">AI Ranking</h3>
            <p className="text-gray-600">
              Advanced ranking algorithm with text match, recency, and company signals
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="text-3xl mb-4">📊</div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Deduplication</h3>
            <p className="text-gray-600">
              Remove duplicate jobs across multiple sources automatically
            </p>
          </div>
        </div>

        {/* Job Sources Section */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Job Sources</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-medium text-green-600 mb-2">✅ Enabled Sources</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Greenhouse (Airbnb, Stripe, Discord, etc.)</li>
                <li>• Lever (Uber, Lyft, Square, etc.)</li>
                <li>• Y Combinator Jobs (RSS feed)</li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-medium text-red-600 mb-2">❌ Disabled Sources</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• LinkedIn (ToS compliance)</li>
                <li>• Glassdoor (ToS compliance)</li>
                <li>• Workday (Coming soon)</li>
                <li>• USAJobs (Coming soon)</li>
              </ul>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-gray-500">
            <p>🚀 Internship Finder - Find your dream internship</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
