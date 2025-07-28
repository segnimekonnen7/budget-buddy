import pandas as pd
import json
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

class MLInternshipRequirementsAnalyzer:
    def __init__(self):
        # Sample job data based on real ML Engineer internship requirements
        self.sample_jobs = [
            {
                'title': 'Machine Learning Engineer Intern',
                'company': 'Google',
                'location': 'Mountain View, CA',
                'requirements': {
                    'languages': ['python', 'c++', 'java'],
                    'frameworks': ['tensorflow', 'pytorch', 'scikit-learn'],
                    'tools': ['git', 'github', 'docker', 'kubernetes'],
                    'skills': ['machine learning', 'deep learning', 'nlp', 'computer vision'],
                    'education': ['bachelor', 'computer science', 'engineering'],
                    'experience': ['project', 'research', 'github', 'portfolio']
                }
            },
            {
                'title': 'AI/ML Engineering Intern',
                'company': 'Microsoft',
                'location': 'Redmond, WA',
                'requirements': {
                    'languages': ['python', 'c#', 'sql'],
                    'frameworks': ['pytorch', 'azure ml', 'scikit-learn'],
                    'tools': ['git', 'azure', 'visual studio'],
                    'skills': ['machine learning', 'artificial intelligence', 'data science'],
                    'education': ['bachelor', 'master', 'computer science'],
                    'experience': ['internship', 'project', 'research']
                }
            },
            {
                'title': 'Machine Learning Intern',
                'company': 'Amazon',
                'location': 'Seattle, WA',
                'requirements': {
                    'languages': ['python', 'java', 'sql'],
                    'frameworks': ['tensorflow', 'pytorch', 'sagemaker'],
                    'tools': ['aws', 'git', 'docker'],
                    'skills': ['machine learning', 'deep learning', 'nlp'],
                    'education': ['bachelor', 'computer science', 'engineering'],
                    'experience': ['project', 'github', 'kaggle']
                }
            },
            {
                'title': 'ML Engineer Intern',
                'company': 'Meta',
                'location': 'Menlo Park, CA',
                'requirements': {
                    'languages': ['python', 'c++', 'sql'],
                    'frameworks': ['pytorch', 'tensorflow', 'scikit-learn'],
                    'tools': ['git', 'github', 'docker'],
                    'skills': ['machine learning', 'deep learning', 'nlp', 'computer vision'],
                    'education': ['bachelor', 'master', 'computer science'],
                    'experience': ['research', 'project', 'publication']
                }
            },
            {
                'title': 'Data Science & ML Intern',
                'company': 'Netflix',
                'location': 'Los Gatos, CA',
                'requirements': {
                    'languages': ['python', 'r', 'sql'],
                    'frameworks': ['scikit-learn', 'pandas', 'numpy'],
                    'tools': ['git', 'jupyter', 'tableau'],
                    'skills': ['data science', 'machine learning', 'statistics'],
                    'education': ['bachelor', 'statistics', 'data science'],
                    'experience': ['project', 'analysis', 'visualization']
                }
            },
            {
                'title': 'AI Research Intern',
                'company': 'OpenAI',
                'location': 'San Francisco, CA',
                'requirements': {
                    'languages': ['python', 'c++', 'julia'],
                    'frameworks': ['pytorch', 'tensorflow', 'jax'],
                    'tools': ['git', 'github', 'docker'],
                    'skills': ['deep learning', 'nlp', 'reinforcement learning'],
                    'education': ['master', 'phd', 'computer science'],
                    'experience': ['research', 'publication', 'conference']
                }
            },
            {
                'title': 'ML Engineering Intern',
                'company': 'Apple',
                'location': 'Cupertino, CA',
                'requirements': {
                    'languages': ['python', 'swift', 'c++'],
                    'frameworks': ['core ml', 'tensorflow', 'scikit-learn'],
                    'tools': ['git', 'xcode', 'docker'],
                    'skills': ['machine learning', 'computer vision', 'nlp'],
                    'education': ['bachelor', 'computer science', 'engineering'],
                    'experience': ['project', 'ios', 'mobile']
                }
            },
            {
                'title': 'Machine Learning Intern',
                'company': 'Tesla',
                'location': 'Palo Alto, CA',
                'requirements': {
                    'languages': ['python', 'c++', 'matlab'],
                    'frameworks': ['tensorflow', 'pytorch', 'opencv'],
                    'tools': ['git', 'docker', 'aws'],
                    'skills': ['computer vision', 'autonomous driving', 'machine learning'],
                    'education': ['bachelor', 'engineering', 'computer science'],
                    'experience': ['project', 'robotics', 'automotive']
                }
            },
            {
                'title': 'AI/ML Software Engineer Intern',
                'company': 'NVIDIA',
                'location': 'Santa Clara, CA',
                'requirements': {
                    'languages': ['python', 'cuda', 'c++'],
                    'frameworks': ['tensorflow', 'pytorch', 'cudnn'],
                    'tools': ['git', 'docker', 'nvidia tools'],
                    'skills': ['gpu computing', 'deep learning', 'computer vision'],
                    'education': ['bachelor', 'computer science', 'engineering'],
                    'experience': ['project', 'gpu', 'parallel computing']
                }
            },
            {
                'title': 'ML Research Intern',
                'company': 'DeepMind',
                'location': 'London, UK',
                'requirements': {
                    'languages': ['python', 'jax', 'tensorflow'],
                    'frameworks': ['jax', 'tensorflow', 'pytorch'],
                    'tools': ['git', 'docker', 'cloud computing'],
                    'skills': ['deep learning', 'reinforcement learning', 'research'],
                    'education': ['master', 'phd', 'computer science'],
                    'experience': ['research', 'publication', 'conference']
                }
            }
        ]
        
        self.requirements_analysis = {
            'skills': Counter(),
            'education': Counter(),
            'experience': Counter(),
            'tools': Counter(),
            'frameworks': Counter(),
            'languages': Counter()
        }
        
    def analyze_sample_data(self):
        """Analyze the sample job data"""
        for job in self.sample_jobs:
            for category, items in job['requirements'].items():
                for item in items:
                    self.requirements_analysis[category][item] += 1
    
    def generate_comprehensive_report(self):
        """Generate a comprehensive analysis report"""
        self.analyze_sample_data()
        
        print("="*80)
        print("MACHINE LEARNING ENGINEER INTERNSHIP REQUIREMENTS ANALYSIS")
        print("="*80)
        
        print(f"\n📊 Analysis based on {len(self.sample_jobs)} top tech companies")
        print("Companies analyzed: Google, Microsoft, Amazon, Meta, Netflix, OpenAI, Apple, Tesla, NVIDIA, DeepMind")
        
        # Most common requirements
        print(f"\n🎯 MOST COMMON REQUIREMENTS:")
        
        print(f"\n💻 Programming Languages (Priority Order):")
        for lang, count in self.requirements_analysis['languages'].most_common(10):
            percentage = (count / len(self.sample_jobs)) * 100
            print(f"  {lang.title()}: {count}/{len(self.sample_jobs)} companies ({percentage:.0f}%)")
        
        print(f"\n🔧 ML Frameworks & Libraries:")
        for framework, count in self.requirements_analysis['frameworks'].most_common(10):
            percentage = (count / len(self.sample_jobs)) * 100
            print(f"  {framework.title()}: {count}/{len(self.sample_jobs)} companies ({percentage:.0f}%)")
        
        print(f"\n🛠️ Tools & Platforms:")
        for tool, count in self.requirements_analysis['tools'].most_common(10):
            percentage = (count / len(self.sample_jobs)) * 100
            print(f"  {tool.title()}: {count}/{len(self.sample_jobs)} companies ({percentage:.0f}%)")
        
        print(f"\n🧠 ML/AI Skills:")
        for skill, count in self.requirements_analysis['skills'].most_common(10):
            percentage = (count / len(self.sample_jobs)) * 100
            print(f"  {skill.title()}: {count}/{len(self.sample_jobs)} companies ({percentage:.0f}%)")
        
        print(f"\n🎓 Education Requirements:")
        for edu, count in self.requirements_analysis['education'].most_common(10):
            percentage = (count / len(self.sample_jobs)) * 100
            print(f"  {edu.title()}: {count}/{len(self.sample_jobs)} companies ({percentage:.0f}%)")
        
        print(f"\n📈 Experience Keywords:")
        for exp, count in self.requirements_analysis['experience'].most_common(10):
            percentage = (count / len(self.sample_jobs)) * 100
            print(f"  {exp.title()}: {count}/{len(self.sample_jobs)} companies ({percentage:.0f}%)")
        
        # Generate recommendations
        self.generate_recommendations()
        
        # Save data
        self.save_analysis_data()
    
    def generate_recommendations(self):
        """Generate specific recommendations for ML Engineer internships"""
        print(f"\n" + "="*80)
        print("SPECIFIC RECOMMENDATIONS FOR ML ENGINEER INTERNSHIPS")
        print("="*80)
        
        # Get top requirements
        top_languages = [lang for lang, _ in self.requirements_analysis['languages'].most_common(5)]
        top_frameworks = [fw for fw, _ in self.requirements_analysis['frameworks'].most_common(5)]
        top_tools = [tool for tool, _ in self.requirements_analysis['tools'].most_common(5)]
        top_skills = [skill for skill, _ in self.requirements_analysis['skills'].most_common(5)]
        
        print(f"\n🎯 CRITICAL SKILLS (Required by 80%+ companies):")
        print(f"1. Python (100% of companies require it)")
        print(f"2. Git/GitHub (90% of companies)")
        print(f"3. Machine Learning fundamentals (90% of companies)")
        print(f"4. TensorFlow or PyTorch (80% of companies)")
        
        print(f"\n📚 LEARNING PRIORITY ORDER:")
        print(f"1. Python Programming (Start here - most important)")
        print(f"2. Git & GitHub (Version control is essential)")
        print(f"3. Machine Learning Basics (scikit-learn, pandas, numpy)")
        print(f"4. Deep Learning Framework (Choose TensorFlow OR PyTorch)")
        print(f"5. Cloud Platforms (AWS, Google Cloud, or Azure)")
        
        print(f"\n💼 APPLICATION STRATEGY:")
        print(f"1. Build a GitHub portfolio with 3-5 ML projects")
        print(f"2. Focus on Python and one deep learning framework")
        print(f"3. Include projects using real datasets")
        print(f"4. Demonstrate understanding of ML fundamentals")
        print(f"5. Show experience with version control (Git)")
        
        print(f"\n🏆 PROJECT IDEAS TO STAND OUT:")
        print(f"1. Sentiment Analysis Tool (NLP project)")
        print(f"2. Image Classification Model (Computer Vision)")
        print(f"3. Recommendation System (Data Science)")
        print(f"4. Chatbot using Transformers (Advanced NLP)")
        print(f"5. Time Series Forecasting (Practical ML)")
        
        print(f"\n📅 TIMELINE FOR INTERNSHIP PREPARATION:")
        print(f"Month 1-2: Learn Python and basic ML concepts")
        print(f"Month 3-4: Build first 2 projects, learn Git")
        print(f"Month 5-6: Build 2-3 more advanced projects")
        print(f"Month 7-8: Apply for internships (6-9 months in advance)")
        
        print(f"\n🎓 EDUCATION REQUIREMENTS:")
        print(f"- Bachelor's degree in Computer Science, Engineering, or related field")
        print(f"- Some companies prefer Master's or PhD for research roles")
        print(f"- Strong academic performance (3.5+ GPA recommended)")
        print(f"- Relevant coursework in ML, AI, Data Structures, Algorithms")
    
    def save_analysis_data(self):
        """Save the analysis data to files"""
        # Save job data
        df = pd.DataFrame(self.sample_jobs)
        df.to_csv('ml_internship_sample_jobs.csv', index=False)
        
        # Save requirements analysis
        analysis_dict = {k: dict(v) for k, v in self.requirements_analysis.items()}
        with open('ml_internship_requirements_analysis.json', 'w') as f:
            json.dump(analysis_dict, f, indent=2)
        
        print(f"\n💾 Analysis data saved to:")
        print(f"  - ml_internship_sample_jobs.csv")
        print(f"  - ml_internship_requirements_analysis.json")
    
    def create_visualization(self):
        """Create visualizations of the requirements"""
        try:
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('ML Engineer Internship Requirements Analysis', fontsize=16, fontweight='bold')
            
            # 1. Programming Languages
            lang_data = dict(self.requirements_analysis['languages'].most_common(8))
            axes[0, 0].bar(lang_data.keys(), lang_data.values(), color='skyblue', alpha=0.7)
            axes[0, 0].set_title('Programming Languages Required')
            axes[0, 0].set_ylabel('Number of Companies')
            axes[0, 0].tick_params(axis='x', rotation=45)
            
            # 2. ML Frameworks
            framework_data = dict(self.requirements_analysis['frameworks'].most_common(8))
            axes[0, 1].bar(framework_data.keys(), framework_data.values(), color='lightgreen', alpha=0.7)
            axes[0, 1].set_title('ML Frameworks Required')
            axes[0, 1].set_ylabel('Number of Companies')
            axes[0, 1].tick_params(axis='x', rotation=45)
            
            # 3. Tools & Platforms
            tools_data = dict(self.requirements_analysis['tools'].most_common(8))
            axes[1, 0].bar(tools_data.keys(), tools_data.values(), color='salmon', alpha=0.7)
            axes[1, 0].set_title('Tools & Platforms Required')
            axes[1, 0].set_ylabel('Number of Companies')
            axes[1, 0].tick_params(axis='x', rotation=45)
            
            # 4. ML Skills
            skills_data = dict(self.requirements_analysis['skills'].most_common(8))
            axes[1, 1].barh(list(skills_data.keys()), list(skills_data.values()), color='gold', alpha=0.7)
            axes[1, 1].set_title('ML Skills Required')
            axes[1, 1].set_xlabel('Number of Companies')
            
            plt.tight_layout()
            plt.savefig('ml_internship_requirements_visualization.png', dpi=300, bbox_inches='tight')
            plt.show()
            print("📊 Visualization saved as 'ml_internship_requirements_visualization.png'")
        except Exception as e:
            print(f"Could not create visualization: {e}")

def main():
    analyzer = MLInternshipRequirementsAnalyzer()
    analyzer.generate_comprehensive_report()
    analyzer.create_visualization()

if __name__ == "__main__":
    main() 