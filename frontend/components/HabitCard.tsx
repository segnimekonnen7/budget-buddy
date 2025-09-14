'use client'

import { useState } from 'react'
import { CheckCircle, Clock, Target, Zap } from 'lucide-react'
import ProgressRing from './ProgressRing'

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

interface HabitCardProps {
  habit: HabitSummary
  onCheckin: () => void
  onSnooze: () => void
}

export default function HabitCard({ habit, onCheckin, onSnooze }: HabitCardProps) {
  const [isLoading, setIsLoading] = useState(false)

  const handleCheckin = async () => {
    setIsLoading(true)
    try {
      await onCheckin()
    } finally {
      setIsLoading(false)
    }
  }

  const handleSnooze = async () => {
    setIsLoading(true)
    try {
      await onSnooze()
    } finally {
      setIsLoading(false)
    }
  }

  const getGoalTypeIcon = () => {
    switch (habit.goal_type) {
      case 'check':
        return <CheckCircle className="h-5 w-5 text-success-600" />
      case 'count':
        return <Target className="h-5 w-5 text-primary-600" />
      case 'duration':
        return <Clock className="h-5 w-5 text-warning-600" />
      default:
        return <Target className="h-5 w-5 text-gray-600" />
    }
  }

  const getGoalTypeText = () => {
    switch (habit.goal_type) {
      case 'check':
        return 'Check off'
      case 'count':
        return `Count: ${habit.target_value || 1}`
      case 'duration':
        return `Duration: ${habit.target_value || 30} min`
      default:
        return 'Complete'
    }
  }

  return (
    <div className="card hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          {getGoalTypeIcon()}
          <div>
            <h3 className="font-semibold text-gray-900">{habit.title}</h3>
            <p className="text-sm text-gray-500">{getGoalTypeText()}</p>
          </div>
        </div>
        
        {habit.best_hour && (
          <div className="flex items-center gap-1 text-xs bg-primary-50 text-primary-700 px-2 py-1 rounded-full">
            <Zap className="h-3 w-3" />
            {habit.best_hour}:00
          </div>
        )}
      </div>

      {habit.notes && (
        <p className="text-sm text-gray-600 mb-4">{habit.notes}</p>
      )}

      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-500">Streak:</span>
          <span className="font-semibold text-gray-900">{habit.current_streak_length} days</span>
        </div>
        
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-500">Grace:</span>
          <span className="text-sm text-gray-900">{habit.grace_per_week}/week</span>
        </div>
      </div>

      <div className="flex items-center justify-center mb-4">
        <ProgressRing
          size={60}
          strokeWidth={4}
          progress={habit.current_streak_length > 0 ? 100 : 0}
          color={habit.current_streak_length > 0 ? '#22c55e' : '#e5e7eb'}
        />
      </div>

      {habit.is_due_today && (
        <div className="flex gap-2">
          <button
            onClick={handleCheckin}
            disabled={isLoading}
            className="btn btn-success flex-1 flex items-center justify-center gap-2"
          >
            <CheckCircle className="h-4 w-4" />
            {isLoading ? 'Checking in...' : 'Check In'}
          </button>
          
          <button
            onClick={handleSnooze}
            disabled={isLoading}
            className="btn btn-secondary flex items-center justify-center gap-2"
          >
            <Clock className="h-4 w-4" />
            Snooze
          </button>
        </div>
      )}

      {!habit.is_due_today && (
        <div className="text-center">
          <p className="text-sm text-gray-500">Not due today</p>
        </div>
      )}
    </div>
  )
}
