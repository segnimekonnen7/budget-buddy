'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import axios from 'axios'
import { ArrowLeft, Save } from 'lucide-react'

export default function NewHabit() {
  const [formData, setFormData] = useState({
    title: '',
    notes: '',
    goal_type: 'check',
    target_value: '',
    grace_per_week: 1,
    timezone: 'UTC'
  })
  const [schedule, setSchedule] = useState({
    type: 'daily',
    days: [1, 2, 3, 4, 5, 6, 7],
    times: ['morning'],
    count: 3
  })
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      await axios.post('https://routine-h9ig.onrender.com/habits', {
        ...formData,
        target_value: formData.target_value ? parseFloat(formData.target_value) : null,
        schedule_json: schedule
      })
      router.push('/')
    } catch (error) {
      console.error('Error creating habit:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const handleScheduleChange = (field: string, value: any) => {
    setSchedule(prev => ({ ...prev, [field]: value }))
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center py-6">
            <button
              onClick={() => router.back()}
              className="mr-4 p-2 hover:bg-gray-100 rounded-lg"
            >
              <ArrowLeft className="h-5 w-5" />
            </button>
            <h1 className="text-3xl font-bold text-gray-900">New Habit</h1>
          </div>
        </div>
      </header>

      {/* Form */}
      <main className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Basic Information</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Habit Title
                </label>
                <input
                  type="text"
                  required
                  value={formData.title}
                  onChange={(e) => handleInputChange('title', e.target.value)}
                  className="input"
                  placeholder="e.g., Drink 8 glasses of water"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Notes (Optional)
                </label>
                <textarea
                  value={formData.notes}
                  onChange={(e) => handleInputChange('notes', e.target.value)}
                  className="input"
                  rows={3}
                  placeholder="Additional notes about this habit..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Goal Type
                </label>
                <select
                  value={formData.goal_type}
                  onChange={(e) => handleInputChange('goal_type', e.target.value)}
                  className="input"
                >
                  <option value="check">Check off (Yes/No)</option>
                  <option value="count">Count (Number)</option>
                  <option value="duration">Duration (Minutes)</option>
                </select>
              </div>

              {(formData.goal_type === 'count' || formData.goal_type === 'duration') && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Target Value
                  </label>
                  <input
                    type="number"
                    value={formData.target_value}
                    onChange={(e) => handleInputChange('target_value', e.target.value)}
                    className="input"
                    placeholder={formData.goal_type === 'count' ? '8' : '30'}
                  />
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Grace Days Per Week
                </label>
                <input
                  type="number"
                  min="0"
                  max="7"
                  value={formData.grace_per_week}
                  onChange={(e) => handleInputChange('grace_per_week', parseInt(e.target.value))}
                  className="input"
                />
                <p className="text-sm text-gray-500 mt-1">
                  Number of days you can miss per week without breaking your streak
                </p>
              </div>
            </div>
          </div>

          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Schedule</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Schedule Type
                </label>
                <select
                  value={schedule.type}
                  onChange={(e) => handleScheduleChange('type', e.target.value)}
                  className="input"
                >
                  <option value="daily">Daily</option>
                  <option value="weekly">Specific Days</option>
                  <option value="times_per_week">Times Per Week</option>
                </select>
              </div>

              {schedule.type === 'weekly' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Days of the Week
                  </label>
                  <div className="grid grid-cols-7 gap-2">
                    {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map((day, index) => (
                      <label key={day} className="flex items-center">
                        <input
                          type="checkbox"
                          checked={schedule.days.includes(index + 1)}
                          onChange={(e) => {
                            const dayNum = index + 1
                            const newDays = e.target.checked
                              ? [...schedule.days, dayNum]
                              : schedule.days.filter(d => d !== dayNum)
                            handleScheduleChange('days', newDays)
                          }}
                          className="mr-2"
                        />
                        <span className="text-sm">{day}</span>
                      </label>
                    ))}
                  </div>
                </div>
              )}

              {schedule.type === 'times_per_week' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Times Per Week
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="7"
                    value={schedule.count || 3}
                    onChange={(e) => handleScheduleChange('count', parseInt(e.target.value))}
                    className="input"
                  />
                </div>
              )}
            </div>
          </div>

          <div className="flex justify-end gap-4">
            <button
              type="button"
              onClick={() => router.back()}
              className="btn btn-secondary"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="btn btn-primary flex items-center gap-2"
            >
              <Save className="h-4 w-4" />
              {loading ? 'Creating...' : 'Create Habit'}
            </button>
          </div>
        </form>
      </main>
    </div>
  )
}
