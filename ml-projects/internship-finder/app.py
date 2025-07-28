#!/usr/bin/env python3
"""
Flask web application for Internship Finder
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from internship_finder import InternshipFinder
import json
import os

app = Flask(__name__)
finder = InternshipFinder()

# Initialize with default user profile
default_profile = {
    'name': 'Segni Mekonnen',
    'skills': ['python', 'machine learning', 'tensorflow', 'pandas', 'scikit-learn', 'git'],
    'preferred_location': 'Remote',
    'remote_preferred': True,
    'min_salary': 20,
    'experience_level': 'Intern'
}
finder.set_user_profile(default_profile)

@app.route('/')
def home():
    """Home page with job search interface"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_jobs():
    """Search for jobs based on criteria"""
    try:
        data = request.get_json()
        keywords = data.get('keywords', 'machine learning intern')
        location = data.get('location', 'remote')
        limit = data.get('limit', 50)
        
        # Scrape jobs
        jobs = finder.scrape_all_sources(keywords, location, limit)
        
        # Filter jobs
        filtered_jobs = finder.filter_jobs()
        
        return jsonify({
            'success': True,
            'jobs': filtered_jobs,
            'total_found': len(filtered_jobs)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/jobs')
def view_jobs():
    """View all available jobs"""
    jobs = finder.get_job_recommendations(20)
    return render_template('jobs.html', jobs=jobs)

@app.route('/job/<int:job_id>')
def job_detail(job_id):
    """View detailed job information"""
    jobs = finder.filtered_jobs
    if 0 <= job_id < len(jobs):
        job = jobs[job_id]
        tips = finder.generate_application_tips(job)
        return render_template('job_detail.html', job=job, tips=tips, job_id=job_id)
    return redirect(url_for('jobs'))

@app.route('/apply/<int:job_id>', methods=['POST'])
def apply_job(job_id):
    """Track job application"""
    try:
        jobs = finder.filtered_jobs
        if 0 <= job_id < len(jobs):
            job = jobs[job_id]
            status = request.form.get('status', 'applied')
            notes = request.form.get('notes', '')
            
            finder.track_application(job, status, notes)
            
            return jsonify({
                'success': True,
                'message': f'Application tracked for {job["title"]} at {job["company"]}'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/applications')
def view_applications():
    """View application tracking"""
    stats = finder.get_application_stats()
    return render_template('applications.html', stats=stats)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """Manage user profile"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            finder.set_user_profile(data)
            return jsonify({
                'success': True,
                'message': 'Profile updated successfully'
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })
    
    return render_template('profile.html', profile=finder.user_profile)

@app.route('/export')
def export_jobs():
    """Export jobs to CSV"""
    try:
        filename = "ml_internships.csv"
        finder.export_jobs_to_csv(filename)
        return jsonify({
            'success': True,
            'message': f'Jobs exported to {filename}',
            'filename': filename
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/stats')
def get_stats():
    """Get application statistics"""
    stats = finder.get_application_stats()
    return jsonify(stats)

@app.route('/api/jobs')
def api_jobs():
    """API endpoint for jobs"""
    jobs = finder.get_job_recommendations(10)
    return jsonify(jobs)

@app.route('/api/job/<int:job_id>')
def api_job_detail(job_id):
    """API endpoint for job details"""
    jobs = finder.filtered_jobs
    if 0 <= job_id < len(jobs):
        job = jobs[job_id]
        tips = finder.generate_application_tips(job)
        return jsonify({
            'job': job,
            'tips': tips
        })
    return jsonify({'error': 'Job not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 