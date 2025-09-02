# 🚀 Habit Loop - Science-backed Habit Builder

A full-stack habit tracking application built with FastAPI backend and enhanced frontend, featuring ML-powered insights and adaptive reminders.

## 🌟 Live Demo

**Frontend:** [https://segnimekonnen7.github.io/budget-buddy/](https://segnimekonnen7.github.io/budget-buddy/)  
**Backend API:** [https://routine-h9ig.onrender.com](https://routine-h9ig.onrender.com)

## 🚀 Features

### 🤖 ML-Powered Insights
- **Success Prediction** - AI-powered habit success likelihood
- **Optimal Reminder Times** - Smart timing recommendations based on completion patterns
- **Completion Statistics** - Detailed habit performance analytics
- **Personalized Recommendations** - Data-driven suggestions for habit improvement

### 🎯 Smart Habit Tracking
- **Flexible Goal Types** - Daily check-in, count-based, duration-based
- **Adaptive Scheduling** - Grace periods and flexible timing
- **Progress Analytics** - Visual streak tracking and completion rates
- **Smart Notifications** - Optimal reminder timing using ML

### 🎨 Modern UI/UX
- **Beautiful Interface** - Professional gradients and animations
- **Responsive Design** - Works perfectly on all devices
- **Interactive Charts** - Progress visualization with Chart.js
- **Tabbed Navigation** - Organized feature sections

## 🏗️ Architecture

- **Backend:** FastAPI with Python 3.11+
- **Frontend:** Vanilla HTML/CSS/JavaScript with modern design
- **Database:** SQLAlchemy with SQLite (local) / PostgreSQL (production)
- **ML Features:** Statistical analysis and rule-based predictions
- **Deployment:** Render.com (backend) + GitHub Pages (frontend)

## 📁 Project Structure

```
budget-buddy/
├── index.html              # Enhanced frontend with ML features
├── .github/workflows/      # GitHub Pages deployment
├── habit-loop/            # Backend FastAPI application
│   ├── backend/           # FastAPI backend
│   │   ├── app/          # Application code
│   │   │   ├── core/     # Configuration and settings
│   │   │   ├── models/   # SQLAlchemy models
│   │   │   ├── routers/  # API routes
│   │   │   └── services/ # Business logic and ML services
│   │   └── requirements.txt
│   ├── main.py           # Deployment entry point
│   ├── Dockerfile        # Container configuration
│   └── render.yaml       # Render deployment config
└── README.md
```

## 🛠️ Local Development

### Backend Setup
```bash
cd habit-loop/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
export PYTHONPATH=.
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend Setup
```bash
# Simply open index.html in your browser
# Or serve with a local server:
python -m http.server 8000
# Then visit: http://localhost:8000
```

## 🚀 Deployment

### Backend (Render.com)
- ✅ **Automatically deployed** from GitHub
- ✅ **CORS configured** for GitHub Pages
- ✅ **ML features enabled** and working

### Frontend (GitHub Pages)
- ✅ **Automatically deployed** from master branch
- ✅ **Enhanced UI** with all ML features
- ✅ **Responsive design** for all devices

## 📊 API Endpoints

### Core Endpoints
- `GET /health` - Health check
- `GET /habits` - Get all habits
- `POST /habits` - Create new habit
- `POST /habits/{id}/checkin` - Check in a habit
- `POST /habits/{id}/miss` - Mark habit as missed

### ML-Powered Insights
- `GET /insights/habits/{id}/success-prediction` - Predict habit success
- `GET /insights/habits/{id}/optimal-reminder` - Get optimal reminder time
- `GET /insights/habits/{id}/completion-stats` - Get completion statistics

## 🔧 Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=sqlite:///./habitloop.db

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://segnimekonnen7.github.io

# JWT
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=10080
```

## 🧪 Testing

```bash
# Backend tests
cd habit-loop/backend
pytest

# Test ML features
python test_ml_features.py
```

## 🎯 ML Features Explained

### Success Prediction
- **Rule-based logic** using completion rates and streak length
- **Statistical analysis** of habit patterns
- **Confidence scoring** for predictions
- **Personalized recommendations** based on data

### Optimal Reminder Timing
- **Pattern analysis** of successful completion times
- **Statistical optimization** using completion data
- **Adaptive scheduling** based on user behavior
- **Success rate optimization** for better habit formation

### Completion Statistics
- **Streak tracking** with visual progress
- **Completion rate analysis** over time
- **Pattern recognition** for habit optimization
- **Data-driven insights** for improvement

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m "Add feature"`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter any issues:
- Check the [Issues](https://github.com/segnimekonnen7/budget-buddy/issues) page
- Create a new issue with detailed information
- Check the deployment status on Render.com

## 🎉 Roadmap

- [x] **ML-powered insights** and predictions
- [x] **Enhanced frontend** with modern UI
- [x] **GitHub Pages deployment** with automation
- [x] **Backend deployment** on Render.com
- [ ] User authentication and profiles
- [ ] Habit sharing and social features
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Integration with fitness trackers

---

**Built with ❤️ using FastAPI, modern web technologies, and ML-powered insights.**

**Live Demo:** [https://segnimekonnen7.github.io/budget-buddy/](https://segnimekonnen7.github.io/budget-buddy/)