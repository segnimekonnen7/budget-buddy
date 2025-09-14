from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Optional, Dict
import httpx
from bs4 import BeautifulSoup
import re
import json
from jinja2 import Template
import os
from dotenv import load_dotenv
import openai
import asyncio
from dataclasses import dataclass

load_dotenv()

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./internship_assistant.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class InternshipApplication(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True)
    position_title = Column(String)
    job_url = Column(String)
    application_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Applied")  # Applied, Interview, Rejected, Accepted, Ghosted
    notes = Column(Text)
    cover_letter = Column(Text)
    resume_version = Column(String)
    follow_up_date = Column(DateTime)
    salary_range = Column(String)
    location = Column(String)
    requirements = Column(Text)
    
    # Enhanced tracking fields
    response_time_days = Column(Integer)  # Days to get response
    interview_count = Column(Integer, default=0)
    rejection_reason = Column(Text)
    offer_amount = Column(Float)
    application_source = Column(String)  # LinkedIn, Indeed, Company Website, etc.
    contact_person = Column(String)
    contact_email = Column(String)
    application_method = Column(String)  # Online form, Email, etc.
    
    # AI-generated insights
    company_rating = Column(Float)  # 1-5 stars
    culture_fit_score = Column(Float)  # 1-5 stars
    growth_potential = Column(Float)  # 1-5 stars
    ai_insights = Column(Text)  # AI-generated company analysis
    interview_tips = Column(Text)  # AI-generated interview preparation
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class JobPosting(Base):
    __tablename__ = "job_postings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    location = Column(String)
    url = Column(String, unique=True)
    description = Column(Text)
    requirements = Column(Text)
    salary_range = Column(String)
    posted_date = Column(DateTime)
    source = Column(String)  # LinkedIn, Indeed, etc.
    scraped_at = Column(DateTime, default=datetime.utcnow)
    is_applied = Column(Boolean, default=False)

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    website = Column(String)
    industry = Column(String)
    size = Column(String)
    description = Column(Text)
    culture_notes = Column(Text)
    interview_process = Column(Text)
    benefits = Column(Text)
    research_notes = Column(Text)
    
    # Enhanced company data
    glassdoor_rating = Column(Float)
    glassdoor_reviews_count = Column(Integer)
    average_salary = Column(Float)
    headquarters = Column(String)
    founded_year = Column(Integer)
    employee_count = Column(String)
    revenue = Column(String)
    stock_symbol = Column(String)
    
    # AI-generated insights
    company_strengths = Column(Text)
    company_weaknesses = Column(Text)
    growth_trajectory = Column(Text)
    culture_analysis = Column(Text)
    interview_insights = Column(Text)
    salary_insights = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Interview(Base):
    __tablename__ = "interviews"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, index=True)
    interview_date = Column(DateTime)
    interview_type = Column(String)  # Phone, Video, In-person, Technical
    interviewer_name = Column(String)
    interviewer_title = Column(String)
    questions_asked = Column(Text)
    your_answers = Column(Text)
    feedback_received = Column(Text)
    next_steps = Column(Text)
    preparation_notes = Column(Text)
    outcome = Column(String)  # Passed, Failed, Pending
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# AI Company Research Functions
async def research_company_ai(company_name: str) -> Dict:
    """Use AI to research company information and generate insights"""
    try:
        # This would use OpenAI API in production
        # For demo purposes, we'll simulate AI research
        
        research_prompt = f"""
        Research the company "{company_name}" and provide insights for a software engineering intern candidate:
        
        1. Company Overview (industry, size, recent news)
        2. Culture & Work Environment
        3. Growth Trajectory & Stability
        4. Interview Process Insights
        5. Salary Expectations for interns
        6. Strengths & Potential Concerns
        7. Why it's a good fit for a CS student
        
        Format as structured insights.
        """
        
        # Simulated AI response (in production, use OpenAI API)
        ai_insights = f"""
        **Company Analysis for {company_name}:**
        
        **Overview:** {company_name} is a technology company known for innovation in their industry. They typically hire interns for hands-on experience with real projects.
        
        **Culture:** The company emphasizes collaboration, learning, and professional growth. Interns often work directly with senior engineers and participate in team meetings.
        
        **Growth:** The company is experiencing steady growth and has a strong track record of converting interns to full-time employees.
        
        **Interview Process:** Expect 2-3 rounds including technical questions, behavioral interviews, and possibly a coding challenge.
        
        **Salary Range:** Typical intern salaries range from $20-30/hour depending on location and experience level.
        
        **Strengths:** Great learning opportunities, mentorship programs, and exposure to cutting-edge technology.
        
        **Considerations:** Fast-paced environment, high expectations for self-directed learning.
        """
        
        return {
            "company_rating": 4.2,
            "culture_fit_score": 4.0,
            "growth_potential": 4.5,
            "ai_insights": ai_insights,
            "interview_tips": f"Prepare for technical questions related to your projects. Research {company_name}'s recent products and be ready to discuss how your skills align with their needs.",
            "salary_insights": "Competitive intern compensation with potential for full-time conversion",
            "company_strengths": "Strong mentorship, real project experience, growth opportunities",
            "company_weaknesses": "Fast-paced environment, high expectations"
        }
    except Exception as e:
        print(f"Error in AI research: {e}")
        return {
            "company_rating": 3.5,
            "culture_fit_score": 3.5,
            "growth_potential": 3.5,
            "ai_insights": f"Limited information available for {company_name}. Consider researching their website and recent news.",
            "interview_tips": "Prepare standard technical and behavioral questions. Research the company's mission and recent developments.",
            "salary_insights": "Research typical intern salaries for similar companies in your area",
            "company_strengths": "To be researched",
            "company_weaknesses": "To be researched"
        }

async def generate_interview_prep(company_name: str, position_title: str) -> str:
    """Generate personalized interview preparation tips"""
    try:
        prep_tips = f"""
        **Interview Preparation for {position_title} at {company_name}:**
        
        **Technical Preparation:**
        - Review your portfolio projects and be ready to explain your technical decisions
        - Practice coding problems related to the technologies mentioned in the job description
        - Prepare to discuss your experience with version control, testing, and deployment
        
        **Company Research:**
        - Study {company_name}'s recent products, news, and company culture
        - Understand their mission and how your role contributes to it
        - Research their competitors and market position
        
        **Behavioral Questions:**
        - Prepare STAR method examples for teamwork, problem-solving, and learning
        - Think of specific examples from your projects and coursework
        - Be ready to discuss challenges you've overcome and lessons learned
        
        **Questions to Ask:**
        - What does a typical day look like for an intern in this role?
        - What projects would I be working on?
        - How does the team collaborate and share knowledge?
        - What opportunities are there for learning and growth?
        
        **Logistics:**
        - Test your technology setup (camera, microphone, internet)
        - Prepare a quiet, professional space for video interviews
        - Have your resume and portfolio ready to reference
        """
        return prep_tips
    except Exception as e:
        return f"Standard interview preparation tips for {company_name}. Research the company, practice technical questions, and prepare behavioral examples."

async def analyze_application_trends(db: Session) -> Dict:
    """Analyze application patterns and provide insights"""
    try:
        total_apps = db.query(InternshipApplication).count()
        status_counts = db.query(
            InternshipApplication.status,
            db.func.count(InternshipApplication.id)
        ).group_by(InternshipApplication.status).all()
        
        # Calculate response time statistics
        responded_apps = db.query(InternshipApplication).filter(
            InternshipApplication.response_time_days.isnot(None)
        ).all()
        
        avg_response_time = 0
        if responded_apps:
            avg_response_time = sum(app.response_time_days for app in responded_apps) / len(responded_apps)
        
        # Company analysis
        companies = db.query(InternshipApplication.company_name).distinct().all()
        company_count = len(companies)
        
        insights = f"""
        **Application Analysis:**
        
        **Overall Stats:**
        - Total Applications: {total_apps}
        - Companies Applied To: {company_count}
        - Average Response Time: {avg_response_time:.1f} days
        
        **Status Breakdown:**
        {chr(10).join([f"- {status}: {count}" for status, count in status_counts])}
        
        **Recommendations:**
        - Focus on companies with faster response times
        - Follow up on applications older than {avg_response_time + 7:.0f} days
        - Diversify application sources to increase response rates
        """
        
        return {
            "total_applications": total_apps,
            "company_count": company_count,
            "avg_response_time": avg_response_time,
            "status_breakdown": dict(status_counts),
            "insights": insights
        }
    except Exception as e:
        return {"error": f"Analysis error: {e}"}

# Pydantic models
class ApplicationCreate(BaseModel):
    company_name: str
    position_title: str
    job_url: Optional[str] = None
    notes: Optional[str] = None
    cover_letter: Optional[str] = None
    resume_version: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    salary_range: Optional[str] = None
    location: Optional[str] = None
    requirements: Optional[str] = None

class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
    follow_up_date: Optional[datetime] = None

class ApplicationResponse(BaseModel):
    id: int
    company_name: str
    position_title: str
    job_url: Optional[str]
    application_date: datetime
    status: str
    notes: Optional[str]
    follow_up_date: Optional[datetime]
    salary_range: Optional[str]
    location: Optional[str]
    requirements: Optional[str]
    
    class Config:
        from_attributes = True

class JobPostingResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    url: str
    description: str
    requirements: Optional[str]
    salary_range: Optional[str]
    posted_date: Optional[datetime]
    source: str
    is_applied: bool
    
    class Config:
        from_attributes = True

class CoverLetterRequest(BaseModel):
    company_name: str
    position_title: str
    job_description: str
    your_skills: List[str]
    your_experience: str
    why_interested: str

# FastAPI app
app = FastAPI(title="Internship Application Assistant", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Job scraping functions
async def scrape_linkedin_jobs(keywords: str, location: str = "Minneapolis, MN") -> List[dict]:
    """Scrape LinkedIn for internship postings"""
    jobs = []
    try:
        # Note: This is a simplified example. Real LinkedIn scraping requires more sophisticated handling
        # and may violate their terms of service. This is for educational purposes.
        
        search_url = f"https://www.linkedin.com/jobs/search/?keywords={keywords}&location={location}&f_TPR=r604800"
        
        async with httpx.AsyncClient() as client:
            # In a real implementation, you'd need proper headers, cookies, and possibly a proxy
            # This is just a placeholder structure
            pass
            
    except Exception as e:
        print(f"Error scraping LinkedIn: {e}")
    
    return jobs

async def scrape_indeed_jobs(keywords: str, location: str = "Minneapolis, MN") -> List[dict]:
    """Scrape Indeed for internship postings"""
    jobs = []
    try:
        search_url = f"https://www.indeed.com/jobs?q={keywords}&l={location}&fromage=7"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(search_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Parse job listings (this is a simplified example)
            job_cards = soup.find_all('div', class_='job_seen_beacon')
            
            for card in job_cards[:10]:  # Limit to 10 results
                try:
                    title_elem = card.find('h2', class_='jobTitle')
                    company_elem = card.find('span', class_='companyName')
                    location_elem = card.find('div', class_='companyLocation')
                    
                    if title_elem and company_elem:
                        job = {
                            'title': title_elem.get_text(strip=True),
                            'company': company_elem.get_text(strip=True),
                            'location': location_elem.get_text(strip=True) if location_elem else location,
                            'url': f"https://indeed.com{title_elem.find('a')['href']}" if title_elem.find('a') else None,
                            'source': 'Indeed'
                        }
                        jobs.append(job)
                except Exception as e:
                    continue
                    
    except Exception as e:
        print(f"Error scraping Indeed: {e}")
    
    return jobs

# Cover letter generation
def generate_cover_letter(request: CoverLetterRequest) -> str:
    """Generate a personalized cover letter"""
    
    template = Template("""
Dear Hiring Manager,

I am writing to express my strong interest in the {{ position_title }} position at {{ company_name }}. As a Computer Information Technology student at Minnesota State University, Mankato, with a passion for backend development and enterprise software solutions, I am excited about the opportunity to contribute to your team.

{% if your_skills %}
My technical skills include {{ your_skills | join(', ') }}, which align well with the requirements for this position. {% endif %}

{% if your_experience %}
{{ your_experience }} {% endif %}

{% if why_interested %}
{{ why_interested }} {% endif %}

I would welcome the opportunity to discuss how my technical skills and passion for software development can contribute to {{ company_name }}'s continued success. Thank you for considering my application, and I look forward to hearing from you.

Sincerely,
Segni Mekonnen
""")
    
    return template.render(
        position_title=request.position_title,
        company_name=request.company_name,
        your_skills=request.your_skills,
        your_experience=request.your_experience,
        why_interested=request.why_interested
    )

# API Endpoints
@app.get("/")
async def root():
    return {"message": "Internship Application Assistant API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# Application management
@app.post("/applications/", response_model=ApplicationResponse)
async def create_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    db_application = InternshipApplication(**application.dict())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

@app.get("/applications/", response_model=List[ApplicationResponse])
async def get_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    applications = db.query(InternshipApplication).offset(skip).limit(limit).all()
    return applications

@app.get("/applications/{application_id}", response_model=ApplicationResponse)
async def get_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(InternshipApplication).filter(InternshipApplication.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

@app.put("/applications/{application_id}", response_model=ApplicationResponse)
async def update_application(application_id: int, application_update: ApplicationUpdate, db: Session = Depends(get_db)):
    application = db.query(InternshipApplication).filter(InternshipApplication.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    for field, value in application_update.dict(exclude_unset=True).items():
        setattr(application, field, value)
    
    application.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(application)
    return application

@app.delete("/applications/{application_id}")
async def delete_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(InternshipApplication).filter(InternshipApplication.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    db.delete(application)
    db.commit()
    return {"message": "Application deleted successfully"}

# Job scraping endpoints
@app.get("/jobs/scrape")
async def scrape_jobs(keywords: str = "software engineering internship", location: str = "Minneapolis, MN"):
    """Scrape job postings from various sources"""
    all_jobs = []
    
    # Scrape from different sources
    indeed_jobs = await scrape_indeed_jobs(keywords, location)
    all_jobs.extend(indeed_jobs)
    
    # Add more sources as needed
    
    return {"jobs": all_jobs, "total": len(all_jobs)}

@app.get("/jobs/", response_model=List[JobPostingResponse])
async def get_job_postings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    job_postings = db.query(JobPosting).offset(skip).limit(limit).all()
    return job_postings

# Cover letter generation
@app.post("/cover-letter/generate")
async def generate_cover_letter_endpoint(request: CoverLetterRequest):
    cover_letter = generate_cover_letter(request)
    return {"cover_letter": cover_letter}

# Analytics and insights
@app.get("/analytics/dashboard")
async def get_dashboard_data(db: Session = Depends(get_db)):
    """Get dashboard analytics"""
    total_applications = db.query(InternshipApplication).count()
    applications_by_status = db.query(
        InternshipApplication.status,
        db.func.count(InternshipApplication.id)
    ).group_by(InternshipApplication.status).all()
    
    recent_applications = db.query(InternshipApplication).order_by(
        InternshipApplication.created_at.desc()
    ).limit(5).all()
    
    return {
        "total_applications": total_applications,
        "applications_by_status": dict(applications_by_status),
        "recent_applications": recent_applications
    }

@app.get("/analytics/follow-ups")
async def get_follow_ups(db: Session = Depends(get_db)):
    """Get applications that need follow-up"""
    today = datetime.utcnow().date()
    follow_ups = db.query(InternshipApplication).filter(
        InternshipApplication.follow_up_date <= today,
        InternshipApplication.status.in_(["Applied", "Interview"])
    ).all()
    
    return {"follow_ups": follow_ups}

# New AI-powered endpoints
@app.post("/research/company")
async def research_company(company_name: str, db: Session = Depends(get_db)):
    """Research a company using AI and return insights"""
    try:
        # Check if company already exists in database
        existing_company = db.query(Company).filter(Company.name == company_name).first()
        
        if existing_company and existing_company.ai_insights:
            return {
                "company_name": company_name,
                "company_rating": existing_company.glassdoor_rating,
                "culture_fit_score": 4.0,  # Default
                "growth_potential": 4.0,   # Default
                "ai_insights": existing_company.culture_analysis,
                "interview_tips": existing_company.interview_insights,
                "salary_insights": existing_company.salary_insights,
                "company_strengths": existing_company.company_strengths,
                "company_weaknesses": existing_company.company_weaknesses,
                "cached": True
            }
        
        # Generate new AI research
        research_data = await research_company_ai(company_name)
        
        # Save to database
        if not existing_company:
            company = Company(
                name=company_name,
                glassdoor_rating=research_data["company_rating"],
                culture_analysis=research_data["ai_insights"],
                interview_insights=research_data["interview_tips"],
                salary_insights=research_data["salary_insights"],
                company_strengths=research_data["company_strengths"],
                company_weaknesses=research_data["company_weaknesses"]
            )
            db.add(company)
        else:
            existing_company.glassdoor_rating = research_data["company_rating"]
            existing_company.culture_analysis = research_data["ai_insights"]
            existing_company.interview_insights = research_data["interview_tips"]
            existing_company.salary_insights = research_data["salary_insights"]
            existing_company.company_strengths = research_data["company_strengths"]
            existing_company.company_weaknesses = research_data["company_weaknesses"]
        
        db.commit()
        
        return {
            "company_name": company_name,
            **research_data,
            "cached": False
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research error: {str(e)}")

@app.post("/applications/{application_id}/research")
async def research_application_company(application_id: int, db: Session = Depends(get_db)):
    """Research the company for a specific application and update it with AI insights"""
    try:
        application = db.query(InternshipApplication).filter(InternshipApplication.id == application_id).first()
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")
        
        # Research the company
        research_data = await research_company_ai(application.company_name)
        
        # Update application with AI insights
        application.company_rating = research_data["company_rating"]
        application.culture_fit_score = research_data["culture_fit_score"]
        application.growth_potential = research_data["growth_potential"]
        application.ai_insights = research_data["ai_insights"]
        application.interview_tips = research_data["interview_tips"]
        
        db.commit()
        
        return {
            "message": "Application updated with AI insights",
            "application_id": application_id,
            "insights": research_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research error: {str(e)}")

@app.get("/analytics/insights")
async def get_application_insights(db: Session = Depends(get_db)):
    """Get AI-powered insights about your application patterns"""
    try:
        insights = await analyze_application_trends(db)
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@app.get("/applications/{application_id}/interview-prep")
async def get_interview_prep(application_id: int, db: Session = Depends(get_db)):
    """Get personalized interview preparation for a specific application"""
    try:
        application = db.query(InternshipApplication).filter(InternshipApplication.id == application_id).first()
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")
        
        prep_tips = await generate_interview_prep(application.company_name, application.position_title)
        
        return {
            "application_id": application_id,
            "company_name": application.company_name,
            "position_title": application.position_title,
            "interview_prep": prep_tips
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prep generation error: {str(e)}")

@app.get("/analytics/company-comparison")
async def compare_companies(db: Session = Depends(get_db)):
    """Compare companies you've applied to"""
    try:
        applications = db.query(InternshipApplication).all()
        
        company_stats = {}
        for app in applications:
            if app.company_name not in company_stats:
                company_stats[app.company_name] = {
                    "total_applications": 0,
                    "statuses": {},
                    "avg_rating": 0,
                    "response_times": []
                }
            
            company_stats[app.company_name]["total_applications"] += 1
            company_stats[app.company_name]["statuses"][app.status] = company_stats[app.company_name]["statuses"].get(app.status, 0) + 1
            
            if app.company_rating:
                company_stats[app.company_name]["avg_rating"] = app.company_rating
            
            if app.response_time_days:
                company_stats[app.company_name]["response_times"].append(app.response_time_days)
        
        # Calculate averages
        for company in company_stats:
            if company_stats[company]["response_times"]:
                company_stats[company]["avg_response_time"] = sum(company_stats[company]["response_times"]) / len(company_stats[company]["response_times"])
            else:
                company_stats[company]["avg_response_time"] = None
        
        return {"company_comparison": company_stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison error: {str(e)}")

@app.get("/analytics/success-factors")
async def analyze_success_factors(db: Session = Depends(get_db)):
    """Analyze what factors lead to successful applications"""
    try:
        successful_apps = db.query(InternshipApplication).filter(
            InternshipApplication.status.in_(["Interview", "Accepted"])
        ).all()
        
        failed_apps = db.query(InternshipApplication).filter(
            InternshipApplication.status.in_(["Rejected", "Ghosted"])
        ).all()
        
        analysis = {
            "successful_applications": len(successful_apps),
            "failed_applications": len(failed_apps),
            "success_rate": len(successful_apps) / (len(successful_apps) + len(failed_apps)) * 100 if (len(successful_apps) + len(failed_apps)) > 0 else 0,
            "insights": []
        }
        
        if successful_apps:
            avg_success_rating = sum(app.company_rating for app in successful_apps if app.company_rating) / len([app for app in successful_apps if app.company_rating])
            analysis["insights"].append(f"Successful applications average company rating: {avg_success_rating:.1f}/5")
        
        if failed_apps:
            avg_failed_rating = sum(app.company_rating for app in failed_apps if app.company_rating) / len([app for app in failed_apps if app.company_rating])
            analysis["insights"].append(f"Failed applications average company rating: {avg_failed_rating:.1f}/5")
        
        # Application source analysis
        sources = {}
        for app in successful_apps + failed_apps:
            if app.application_source:
                if app.application_source not in sources:
                    sources[app.application_source] = {"successful": 0, "failed": 0}
                if app.status in ["Interview", "Accepted"]:
                    sources[app.application_source]["successful"] += 1
                else:
                    sources[app.application_source]["failed"] += 1
        
        analysis["source_analysis"] = sources
        
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
