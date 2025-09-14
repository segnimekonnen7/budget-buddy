'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import axios from 'axios'
import { Plus, CheckCircle, Clock, Target } from 'lucide-react'
import HabitCard from '@/components/HabitCard'
import ProgressRing from '@/components/ProgressRing'

interface HabitSummary {
  id: string
  title: string
  notes?: string
  goal_type: string
  target_value?: number
  grace_per_week: number
  timezone: string
  created_at: string
  current_streak_length: number
  is_due_today: boolean
  best_hour?: number
}

export default function Dashboard() {
  const [habits, setHabits] = useState<HabitSummary[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  useEffect(() => {
    fetchHabits()
  }, [])

  const fetchHabits = async () => {
    try {
      const response = await axios.get('https://routine-h9ig.onrender.com/habits')
      setHabits(response.data)
    } catch (err) {
      setError('Failed to load habits')
      console.error('Error fetching habits:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleCheckin = async (habitId: string) => {
    try {
      await axios.post(`https://routine-h9ig.onrender.com/habits/${habitId}/checkin`, {
        ts: new Date().toISOString()
      })
      fetchHabits() // Refresh habits
    } catch (err) {
      console.error('Error checking in:', err)
    }
  }

  const handleSnooze = async (habitId: string) => {
    try {
      await axios.post(`https://routine-h9ig.onrender.com/habits/${habitId}/miss`, {
        ts: new Date().toISOString()
      })
      fetchHabits() // Refresh habits
    } catch (err) {
      console.error('Error snoozing:', err)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <button 
            onClick={fetchHabits}
            className="btn btn-primary"
          >
            Try Again
          </button>
        </div>
      </div>
    )
  }

  const todayHabits = habits.filter(habit => habit.is_due_today)
  const totalHabits = habits.length
  const completedToday = todayHabits.filter(habit => habit.current_streak_length > 0).length

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Habit Loop</h1>
              <p className="text-gray-600">Science-backed habit building</p>
            </div>
            <button
              onClick={() => router.push('/habits/new')}
              className="btn btn-primary flex items-center gap-2"
            >
              <Plus className="h-5 w-5" />
              New Habit
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Today's Overview */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Today's Overview</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="card">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <Target className="h-8 w-8 text-primary-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Total Habits</p>
                  <p className="text-2xl font-bold text-gray-900">{totalHabits}</p>
                </div>
              </div>
            </div>
            
            <div className="card">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <Clock className="h-8 w-8 text-warning-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Due Today</p>
                  <p className="text-2xl font-bold text-gray-900">{todayHabits.length}</p>
                </div>
              </div>
            </div>
            
            <div className="card">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <CheckCircle className="h-8 w-8 text-success-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Completed</p>
                  <p className="text-2xl font-bold text-gray-900">{completedToday}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Today's Habits */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Today's Habits</h2>
          {todayHabits.length === 0 ? (
            <div className="card text-center py-12">
              <p className="text-gray-500">No habits due today. Great job!</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {todayHabits.map((habit) => (
                <HabitCard
                  key={habit.id}
                  habit={habit}
                  onCheckin={() => handleCheckin(habit.id)}
                  onSnooze={() => handleSnooze(habit.id)}
                />
              ))}
            </div>
          )}
        </div>

        {/* All Habits */}
        {habits.length > todayHabits.length && (
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">All Habits</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {habits
                .filter(habit => !habit.is_due_today)
                .map((habit) => (
                  <HabitCard
                    key={habit.id}
                    habit={habit}
                    onCheckin={() => handleCheckin(habit.id)}
                    onSnooze={() => handleSnooze(habit.id)}
                  />
                ))}
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
