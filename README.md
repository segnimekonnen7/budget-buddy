# 🚀 Segni Mekonnen - Portfolio Projects

**Backend Software Engineer | AI/ML Intern @ Outamation | ML Research Assistant**

Welcome to my portfolio repository showcasing three production-ready full-stack applications built with Python, FastAPI, and modern web technologies.

---

## 🌟 Featured Projects

### 1. 🎯 Habit Loop - ML-Powered Habit Tracker

**ML model achieving 96% accuracy | FastAPI + React + PostgreSQL**

A full-stack habit tracking application with machine learning backend that predicts user consistency from historical data. Features real-time predictions, adaptive reminders, and comprehensive analytics.

**🔗 Links:**
- **Live Demo:** [https://segnimekonnen7.github.io/budget-buddy/](https://segnimekonnen7.github.io/budget-buddy/)
- **Backend API:** [https://routine-h9ig.onrender.com](https://routine-h9ig.onrender.com)
- **Project Directory:** [`habit-loop/`](./habit-loop/)

**✨ Key Features:**
- ML prediction model using scikit-learn RandomForestClassifier (96% accuracy, verified 99% test)
- REST APIs with FastAPI and SQLAlchemy
- Real-time success predictions and optimal reminder timing
- React frontend with dynamic charts and progress visualization
- Docker containerization and deployment on Render

**🛠️ Tech Stack:** Python, FastAPI, React, PostgreSQL, scikit-learn, Docker

---

### 2. 💬 Real-Time Chat Application

**WebSocket-based messaging system | FastAPI + WebSockets + SQLAlchemy**

A production-ready real-time messaging system with WebSocket architecture, JWT authentication, and scalable backend. Built as a team project demonstrating real-time systems expertise.

**🔗 Links:**
- **Project Directory:** [`realtime-chat/`](./realtime-chat/)
- **Demo:** [`realtime-chat-demo/`](./realtime-chat-demo/)

**✨ Key Features:**
- WebSocket connection manager with async Python for real-time messaging
- JWT authentication with BCrypt password hashing
- Normalized database schema with SQLAlchemy ORM (Users, Rooms, Messages, Memberships)
- Typing indicators, online user tracking, and persistent message history
- Containerized with Docker for scalable deployment

**🛠️ Tech Stack:** Python, FastAPI, WebSockets, SQLAlchemy, JWT, BCrypt, Docker, Redis

---

### 3. 🌤️ Weather Dashboard API

**Intelligent caching & external API integration | FastAPI + HTTPX**

A production-ready weather dashboard with intelligent caching strategy, comprehensive error handling, and beautiful responsive UI. Demonstrates external API integration and performance optimization.

**🔗 Links:**
- **Project Directory:** [`weather-dashboard/`](./weather-dashboard/)
- **Demo:** [`weather-dashboard-demo/`](./weather-dashboard-demo/)

**✨ Key Features:**
- Intelligent 10-minute caching strategy to reduce external API dependency
- OpenWeatherMap API integration with async HTTP requests
- Location search, 5-day forecasts, and comprehensive error handling
- Responsive UI deployed on GitHub Pages
- Auto-generated API documentation with Swagger UI

**🛠️ Tech Stack:** Python, FastAPI, HTTPX, OpenWeatherMap API, Caching, Docker

---

## 📊 Project Highlights

| Project | ML Accuracy | Tech Stack | Deployment |
|---------|------------|------------|------------|
| **Habit Loop** | 96% (99% test) | FastAPI, React, scikit-learn | Render + GitHub Pages |
| **Real-Time Chat** | Real-time messaging | FastAPI, WebSockets, JWT | Docker |
| **Weather Dashboard** | 10-min caching | FastAPI, HTTPX, OpenWeatherMap | GitHub Pages |

---

## 🛠️ Tech Stack Overview

**Backend:**
- Python 3.11+
- FastAPI (async web framework)
- SQLAlchemy (ORM)
- WebSockets (real-time communication)
- JWT Authentication
- Docker (containerization)

**Frontend:**
- React / Vanilla JavaScript
- HTML5/CSS3
- Responsive design

**ML/AI:**
- scikit-learn (RandomForestClassifier)
- pandas, NumPy
- Feature engineering and cross-validation

**DevOps:**
- Docker
- GitHub Actions
- Render.com deployment
- GitHub Pages

---

## 🚀 Quick Start

### Habit Loop
```bash
cd habit-loop/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Real-Time Chat
```bash
cd realtime-chat
pip install -r requirements.txt
uvicorn main:app --reload
```

### Weather Dashboard
```bash
cd weather-dashboard
export OPENWEATHER_API_KEY="your_key"
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 📁 Repository Structure

```
budget-buddy/
├── habit-loop/              # ML-Powered Habit Tracker
│   ├── backend/            # FastAPI backend
│   └── frontend/           # React frontend
├── realtime-chat/          # Real-Time Chat Application
│   ├── main.py            # FastAPI + WebSockets
│   └── Dockerfile
├── weather-dashboard/      # Weather Dashboard API
│   ├── main.py            # FastAPI + HTTPX
│   └── Dockerfile
└── README.md              # This file
```

---

## 🎯 Key Achievements

- ✅ **ML Model:** Trained RandomForestClassifier achieving 96% accuracy (verified 99% test)
- ✅ **Real-Time Systems:** Built WebSocket-based chat with <100ms message latency
- ✅ **API Optimization:** Designed intelligent caching reducing external API calls by 90%
- ✅ **Full-Stack:** Complete applications from database design to frontend deployment
- ✅ **Production Ready:** All projects containerized and deployed

---

## 📧 Contact

- **Email:** segnimekonnen7@gmail.com
- **LinkedIn:** [linkedin.com/in/segni-mekonnen-16928125b](https://linkedin.com/in/segni-mekonnen-16928125b)
- **GitHub:** [github.com/segnimekonnen7](https://github.com/segnimekonnen7)
- **Portfolio:** [segnimekonnen7.github.io/segni-portfolio-](https://segnimekonnen7.github.io/segni-portfolio-)

---

## 📄 License

This project is licensed under the MIT License.

---

**Built with ❤️ using Python, FastAPI, and modern web technologies.**
