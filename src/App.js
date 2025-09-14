import React, { useState } from 'react';
import { FaGithub, FaLinkedin, FaEnvelope, FaCode, FaDatabase, FaCloud, FaServer, FaDocker, FaAws, FaPython, FaNodeJs } from 'react-icons/fa';
import { SiDjango, SiFlask, SiPostgresql, SiMongodb, SiRedis, SiExpress } from 'react-icons/si';
import './App.css';

function App() {
  const [activeSection, setActiveSection] = useState('about');

  const scrollToSection = (sectionId) => {
    setActiveSection(sectionId);
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="App">
      {/* Navigation */}
      <nav className="navbar">
        <div className="nav-container">
          <div className="nav-logo">
            <h2>Segni Mekonnen</h2>
          </div>
          <ul className="nav-menu">
            <li><a href="#about" onClick={() => scrollToSection('about')} className={activeSection === 'about' ? 'active' : ''}>About</a></li>
            <li><a href="#projects" onClick={() => scrollToSection('projects')} className={activeSection === 'projects' ? 'active' : ''}>Projects</a></li>
            <li><a href="#skills" onClick={() => scrollToSection('skills')} className={activeSection === 'skills' ? 'active' : ''}>Skills</a></li>
            <li><a href="#education" onClick={() => scrollToSection('education')} className={activeSection === 'education' ? 'active' : ''}>Education</a></li>
            <li><a href="#contact" onClick={() => scrollToSection('contact')} className={activeSection === 'contact' ? 'active' : ''}>Contact</a></li>
          </ul>
        </div>
      </nav>

      {/* Hero Section */}
      <section id="about" className="hero">
        <div className="hero-container">
          <div className="hero-content">
            <h1>Segni Mekonnen</h1>
            <h2>Backend Software Engineer</h2>
            <p className="hero-description">
              Aspiring Backend Developer with expertise in Python, Node.js, and database design. 
              Built scalable APIs handling thousands of requests and real-time systems supporting 50+ concurrent users.
            </p>
            <div className="hero-stats">
              <div className="stat">
                <span className="stat-number">50+</span>
                <span className="stat-label">Concurrent Users</span>
              </div>
              <div className="stat">
                <span className="stat-number">20%</span>
                <span className="stat-label">Performance Boost</span>
              </div>
              <div className="stat">
                <span className="stat-number">1000+</span>
                <span className="stat-label">API Requests/Day</span>
              </div>
            </div>
            <div className="hero-buttons">
              <a href="#projects" className="btn btn-primary" onClick={() => scrollToSection('projects')}>View Projects</a>
              <a href="#contact" className="btn btn-secondary" onClick={() => scrollToSection('contact')}>Get In Touch</a>
            </div>
          </div>
          <div className="hero-image">
            <div className="tech-icons">
              <FaPython className="tech-icon" />
              <FaNodeJs className="tech-icon" />
              <SiDjango className="tech-icon" />
              <SiPostgresql className="tech-icon" />
              <FaDocker className="tech-icon" />
              <FaAws className="tech-icon" />
            </div>
          </div>
        </div>
      </section>

      {/* Projects Section */}
      <section id="projects" className="projects">
        <div className="container">
          <h2 className="section-title">Featured Projects</h2>
          <div className="projects-grid">
            <div className="project-card">
              <div className="project-header">
                <h3>Job Board API</h3>
                <div className="project-tech">
                  <span className="tech-tag">Python</span>
                  <span className="tech-tag">Django</span>
                  <span className="tech-tag">PostgreSQL</span>
                  <span className="tech-tag">Redis</span>
                </div>
              </div>
              <p className="project-description">
                Scalable job board backend with JWT authentication, REST APIs, and Redis caching. 
                Handles 1000+ job listings with 20% faster search performance.
              </p>
              <div className="project-features">
                <span className="feature">JWT Authentication</span>
                <span className="feature">REST APIs</span>
                <span className="feature">Redis Caching</span>
                <span className="feature">Docker Deployment</span>
              </div>
              <div className="project-links">
                <a href="#" className="project-link"><FaGithub /> GitHub</a>
                <a href="#" className="project-link"><FaServer /> Live Demo</a>
              </div>
            </div>

            <div className="project-card">
              <div className="project-header">
                <h3>Real-time Collaboration Platform</h3>
                <div className="project-tech">
                  <span className="tech-tag">Node.js</span>
                  <span className="tech-tag">Socket.io</span>
                  <span className="tech-tag">MongoDB</span>
                  <span className="tech-tag">Redis</span>
                </div>
              </div>
              <p className="project-description">
                Real-time collaboration platform with WebSocket connections, live chat, and shared code editing. 
                Supports 50+ concurrent users with sub-300ms response times.
              </p>
              <div className="project-features">
                <span className="feature">WebSocket Connections</span>
                <span className="feature">Live Chat</span>
                <span className="feature">Shared Editing</span>
                <span className="feature">User Sessions</span>
              </div>
              <div className="project-links">
                <a href="#" className="project-link"><FaGithub /> GitHub</a>
                <a href="#" className="project-link"><FaServer /> Live Demo</a>
              </div>
            </div>

            <div className="project-card">
              <div className="project-header">
                <h3>Sentiment Analysis API</h3>
                <div className="project-tech">
                  <span className="tech-tag">Flask</span>
                  <span className="tech-tag">ML</span>
                  <span className="tech-tag">AWS</span>
                  <span className="tech-tag">Docker</span>
                </div>
              </div>
              <p className="project-description">
                Production-ready sentiment analysis API with 97.6% accuracy. 
                Deployed on AWS with rate limiting, monitoring, and processes 500+ requests/day.
              </p>
              <div className="project-features">
                <span className="feature">97.6% Accuracy</span>
                <span className="feature">Rate Limiting</span>
                <span className="feature">Health Monitoring</span>
                <span className="feature">Auto-scaling</span>
              </div>
              <div className="project-links">
                <a href="#" className="project-link"><FaGithub /> GitHub</a>
                <a href="#" className="project-link"><FaServer /> Live Demo</a>
              </div>
            </div>

            <div className="project-card">
              <div className="project-header">
                <h3>E-commerce Backend</h3>
                <div className="project-tech">
                  <span className="tech-tag">Django REST</span>
                  <span className="tech-tag">PostgreSQL</span>
                  <span className="tech-tag">Stripe</span>
                  <span className="tech-tag">Docker</span>
                </div>
              </div>
              <p className="project-description">
                Complete e-commerce backend with product management, order processing, and Stripe payment integration. 
                Complex database schema with secure transaction handling.
              </p>
              <div className="project-features">
                <span className="feature">Payment Integration</span>
                <span className="feature">Inventory Management</span>
                <span className="feature">Order Processing</span>
                <span className="feature">Security</span>
              </div>
              <div className="project-links">
                <a href="#" className="project-link"><FaGithub /> GitHub</a>
                <a href="#" className="project-link"><FaServer /> Live Demo</a>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Skills Section */}
      <section id="skills" className="skills">
        <div className="container">
          <h2 className="section-title">Technical Skills</h2>
          <div className="skills-grid">
            <div className="skill-category">
              <h3><FaCode /> Programming Languages</h3>
              <div className="skill-items">
                <div className="skill-item">
                  <FaPython className="skill-icon" />
                  <span>Python (Advanced)</span>
                </div>
                <div className="skill-item">
                  <FaNodeJs className="skill-icon" />
                  <span>JavaScript (Intermediate)</span>
                </div>
                <div className="skill-item">
                  <FaDatabase className="skill-icon" />
                  <span>SQL (Advanced)</span>
                </div>
              </div>
            </div>

            <div className="skill-category">
              <h3><FaServer /> Backend Frameworks</h3>
              <div className="skill-items">
                <div className="skill-item">
                  <SiDjango className="skill-icon" />
                  <span>Django & Django REST</span>
                </div>
                <div className="skill-item">
                  <SiFlask className="skill-icon" />
                  <span>Flask</span>
                </div>
                <div className="skill-item">
                  <SiExpress className="skill-icon" />
                  <span>Express.js</span>
                </div>
                <div className="skill-item">
                  <FaCode className="skill-icon" />
                  <span>Socket.io</span>
                </div>
              </div>
            </div>

            <div className="skill-category">
              <h3><FaDatabase /> Databases & Storage</h3>
              <div className="skill-items">
                <div className="skill-item">
                  <SiPostgresql className="skill-icon" />
                  <span>PostgreSQL</span>
                </div>
                <div className="skill-item">
                  <SiMongodb className="skill-icon" />
                  <span>MongoDB</span>
                </div>
                <div className="skill-item">
                  <SiRedis className="skill-icon" />
                  <span>Redis</span>
                </div>
              </div>
            </div>

            <div className="skill-category">
              <h3><FaCloud /> DevOps & Deployment</h3>
              <div className="skill-items">
                <div className="skill-item">
                  <FaDocker className="skill-icon" />
                  <span>Docker</span>
                </div>
                <div className="skill-item">
                  <FaAws className="skill-icon" />
                  <span>AWS</span>
                </div>
                <div className="skill-item">
                  <FaCode className="skill-icon" />
                  <span>CI/CD</span>
                </div>
                <div className="skill-item">
                  <FaCode className="skill-icon" />
                  <span>Git</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Education Section */}
      <section id="education" className="education">
        <div className="container">
          <h2 className="section-title">Education & Certifications</h2>
          <div className="education-grid">
            <div className="education-card">
              <h3>B.S. Computer Information Technology</h3>
              <p className="education-school">Minnesota State University, Mankato</p>
              <p className="education-year">Expected 2026</p>
              <div className="education-details">
                <h4>Relevant Coursework:</h4>
                <ul>
                  <li>Database Systems</li>
                  <li>Web Development</li>
                  <li>Software Engineering</li>
                  <li>Data Structures</li>
                </ul>
              </div>
            </div>

            <div className="education-card">
              <h3>Professional Certifications</h3>
              <div className="certifications">
                <div className="cert-item">
                  <FaAws className="cert-icon" />
                  <span>AWS Cloud Practitioner</span>
                </div>
                <div className="cert-item">
                  <FaDocker className="cert-icon" />
                  <span>Docker Certified Associate</span>
                </div>
                <div className="cert-item">
                  <FaCode className="cert-icon" />
                  <span>Meta Back-End Developer (Coursera)</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="contact">
        <div className="container">
          <h2 className="section-title">Get In Touch</h2>
          <div className="contact-content">
            <div className="contact-info">
              <h3>Let's Connect!</h3>
              <p>I'm always interested in new opportunities and exciting projects. Feel free to reach out!</p>
              <div className="contact-links">
                <a href="mailto:your.email@example.com" className="contact-link">
                  <FaEnvelope />
                  <span>your.email@example.com</span>
                </a>
                <a href="https://github.com/segnimekonnen7" className="contact-link">
                  <FaGithub />
                  <span>GitHub</span>
                </a>
                <a href="https://linkedin.com/in/segnimekonnen" className="contact-link">
                  <FaLinkedin />
                  <span>LinkedIn</span>
                </a>
              </div>
            </div>
            <div className="contact-form">
              <form>
                <div className="form-group">
                  <input type="text" placeholder="Your Name" required />
                </div>
                <div className="form-group">
                  <input type="email" placeholder="Your Email" required />
                </div>
                <div className="form-group">
                  <textarea placeholder="Your Message" rows="5" required></textarea>
                </div>
                <button type="submit" className="btn btn-primary">Send Message</button>
              </form>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <p>&copy; 2024 Segni Mekonnen. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
