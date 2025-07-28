import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.preprocessing import StandardScaler
import joblib
import re
from typing import List, Dict, Any, Tuple
import logging

class MLRecommendationSystem:
    """Machine Learning recommendation system for internship matching"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.job_vectors = None
        self.user_profile_vector = None
        self.jobs_df = None
        self.similarity_matrix = None
        self.clustering_model = None
        self.topic_model = None
        self.scaler = StandardScaler()
        
        # Skill importance weights
        self.skill_weights = {
            'python': 0.9,
            'machine learning': 0.95,
            'deep learning': 0.9,
            'tensorflow': 0.85,
            'pytorch': 0.85,
            'scikit-learn': 0.8,
            'pandas': 0.75,
            'numpy': 0.75,
            'sql': 0.7,
            'git': 0.6,
            'docker': 0.7,
            'aws': 0.75,
            'nlp': 0.8,
            'computer vision': 0.8,
            'data science': 0.85,
            'statistics': 0.8,
            'research': 0.7,
            'neural networks': 0.85,
            'reinforcement learning': 0.8,
            'mlops': 0.75
        }
        
        self.logger = logging.getLogger(__name__)
    
    def preprocess_job_data(self, jobs_data: List[Dict]) -> pd.DataFrame:
        """Preprocess job data for ML analysis"""
        df = pd.DataFrame(jobs_data)
        
        # Combine text fields for analysis
        df['combined_text'] = df['title'].fillna('') + ' ' + \
                             df['description'].fillna('') + ' ' + \
                             df['company'].fillna('')
        
        # Extract skills from description
        df['extracted_skills'] = df['description'].apply(self._extract_skills)
        
        # Create skill vectors
        df['skill_vector'] = df['extracted_skills'].apply(self._create_skill_vector)
        
        # Calculate job complexity score
        df['complexity_score'] = df['description'].apply(self._calculate_complexity)
        
        # Extract location features
        df['is_remote'] = df['location'].str.contains('remote|Remote', case=False, na=False)
        df['is_hybrid'] = df['location'].str.contains('hybrid|Hybrid', case=False, na=False)
        
        # Extract salary information
        df['salary_numeric'] = df['salary'].apply(self._extract_salary)
        
        return df
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from job description"""
        if pd.isna(text):
            return []
        
        text_lower = text.lower()
        extracted_skills = []
        
        # Check for skills in the text
        for skill in self.skill_weights.keys():
            if skill in text_lower:
                extracted_skills.append(skill)
        
        # Additional skill extraction patterns
        skill_patterns = {
            'python': r'\bpython\b',
            'java': r'\bjava\b',
            'c\+\+': r'\\bc\+\+\\b',
            'r': r'\br\b',
            'matlab': r'\bmatlab\b',
            'julia': r'\bjulia\b',
            'tensorflow': r'\btensorflow\b',
            'pytorch': r'\bpytorch\b',
            'keras': r'\bkeras\b',
            'scikit-learn': r'\bscikit-learn\b',
            'pandas': r'\bpandas\b',
            'numpy': r'\bnumpy\b',
            'sql': r'\bsql\b',
            'git': r'\bgit\b',
            'docker': r'\bdocker\b',
            'kubernetes': r'\bkubernetes\b',
            'aws': r'\baws\b',
            'azure': r'\bazure\b',
            'gcp': r'\bgcp\b'
        }
        
        for skill, pattern in skill_patterns.items():
            if re.search(pattern, text_lower):
                extracted_skills.append(skill)
        
        return list(set(extracted_skills))
    
    def _create_skill_vector(self, skills: List[str]) -> np.ndarray:
        """Create a skill vector for a job"""
        vector = np.zeros(len(self.skill_weights))
        skill_list = list(self.skill_weights.keys())
        
        for skill in skills:
            if skill in skill_list:
                idx = skill_list.index(skill)
                vector[idx] = self.skill_weights[skill]
        
        return vector
    
    def _calculate_complexity(self, text: str) -> float:
        """Calculate job complexity based on description"""
        if pd.isna(text):
            return 0.0
        
        # Complexity indicators
        complexity_indicators = [
            'research', 'phd', 'thesis', 'publication', 'paper',
            'advanced', 'expert', 'senior', 'lead', 'architect',
            'algorithm', 'optimization', 'scalable', 'distributed',
            'real-time', 'production', 'deployment', 'mlops'
        ]
        
        text_lower = text.lower()
        complexity_score = 0.0
        
        for indicator in complexity_indicators:
            if indicator in text_lower:
                complexity_score += 0.1
        
        return min(complexity_score, 1.0)
    
    def _extract_salary(self, salary_text: str) -> float:
        """Extract numeric salary from text"""
        if pd.isna(salary_text):
            return 0.0
        
        # Extract numbers from salary text
        numbers = re.findall(r'\d+', salary_text)
        if numbers:
            # Take the average if range is given
            return sum(map(int, numbers)) / len(numbers)
        return 0.0
    
    def build_recommendation_model(self, jobs_data: List[Dict]):
        """Build the recommendation model"""
        self.logger.info("Building ML recommendation model...")
        
        # Preprocess data
        self.jobs_df = self.preprocess_job_data(jobs_data)
        
        # Create TF-IDF vectors for text similarity
        self.job_vectors = self.vectorizer.fit_transform(self.jobs_df['combined_text'])
        
        # Create similarity matrix
        self.similarity_matrix = cosine_similarity(self.job_vectors)
        
        # Cluster jobs for category-based recommendations
        self._cluster_jobs()
        
        # Build topic model for content-based filtering
        self._build_topic_model()
        
        self.logger.info("Recommendation model built successfully!")
    
    def _cluster_jobs(self, n_clusters=5):
        """Cluster jobs into categories"""
        # Use skill vectors for clustering
        skill_matrix = np.array(self.jobs_df['skill_vector'].tolist())
        
        # Normalize features
        skill_matrix_scaled = self.scaler.fit_transform(skill_matrix)
        
        # Adjust number of clusters based on data size
        n_clusters = min(n_clusters, len(skill_matrix_scaled))
        
        if n_clusters > 1:
            # Perform clustering
            self.clustering_model = KMeans(n_clusters=n_clusters, random_state=42)
            self.jobs_df['cluster'] = self.clustering_model.fit_predict(skill_matrix_scaled)
        else:
            # If only one sample, assign cluster 0
            self.jobs_df['cluster'] = 0
            self.clustering_model = None
    
    def _build_topic_model(self, n_topics=5):
        """Build topic model for content analysis"""
        # Adjust number of topics based on data size
        n_topics = min(n_topics, self.job_vectors.shape[0])
        
        if n_topics > 1:
            # Use TF-IDF vectors for topic modeling
            self.topic_model = LatentDirichletAllocation(
                n_components=n_topics, 
                random_state=42,
                max_iter=10
            )
            self.topic_model.fit(self.job_vectors)
            
            # Assign topics to jobs
            topic_distributions = self.topic_model.transform(self.job_vectors)
            self.jobs_df['topic'] = topic_distributions.argmax(axis=1)
        else:
            # If only one sample, assign topic 0
            self.jobs_df['topic'] = 0
            self.topic_model = None
    
    def set_user_profile(self, user_profile: Dict[str, Any]):
        """Set user profile for personalized recommendations"""
        # Create user skill vector
        user_skills = user_profile.get('skills', [])
        self.user_profile_vector = self._create_skill_vector(user_skills)
        
        # Create user text vector
        user_text = f"{user_profile.get('name', '')} {user_profile.get('education', '')} {' '.join(user_skills)}"
        user_text_vector = self.vectorizer.transform([user_text])
        
        # Calculate similarity with all jobs
        user_similarities = cosine_similarity(user_text_vector, self.job_vectors).flatten()
        self.jobs_df['user_similarity'] = user_similarities
    
    def get_personalized_recommendations(self, user_profile: Dict[str, Any], n_recommendations: int = 10) -> List[Dict]:
        """Get personalized job recommendations"""
        self.set_user_profile(user_profile)
        
        # Calculate comprehensive recommendation scores
        self.jobs_df['recommendation_score'] = self._calculate_recommendation_scores(user_profile)
        
        # Sort by recommendation score
        top_jobs = self.jobs_df.nlargest(n_recommendations, 'recommendation_score')
        
        # Convert to list of dictionaries
        recommendations = []
        for _, job in top_jobs.iterrows():
            job_dict = job.to_dict()
            job_dict['match_reasons'] = self._get_match_reasons(job, user_profile)
            recommendations.append(job_dict)
        
        return recommendations
    
    def _calculate_recommendation_scores(self, user_profile: Dict[str, Any]) -> np.ndarray:
        """Calculate comprehensive recommendation scores"""
        scores = np.zeros(len(self.jobs_df))
        
        # Skill match score (40% weight)
        user_skills = set(user_profile.get('skills', []))
        for i, job_skills in enumerate(self.jobs_df['extracted_skills']):
            skill_match = len(user_skills.intersection(set(job_skills))) / max(len(job_skills), 1)
            scores[i] += 0.4 * skill_match
        
        # User similarity score (30% weight)
        scores += 0.3 * self.jobs_df['user_similarity']
        
        # Complexity match score (20% weight)
        user_experience = user_profile.get('experience_level', 'beginner')
        complexity_preference = {
            'beginner': 0.3,
            'intermediate': 0.6,
            'advanced': 0.9
        }
        preferred_complexity = complexity_preference.get(user_experience, 0.5)
        
        complexity_scores = 1 - np.abs(self.jobs_df['complexity_score'] - preferred_complexity)
        scores += 0.2 * complexity_scores
        
        # Location preference score (10% weight)
        user_location_pref = user_profile.get('location_preference', 'any')
        if user_location_pref == 'remote':
            location_scores = self.jobs_df['is_remote'].astype(float)
        elif user_location_pref == 'hybrid':
            location_scores = self.jobs_df['is_hybrid'].astype(float)
        else:
            location_scores = np.ones(len(self.jobs_df))  # No preference
        
        scores += 0.1 * location_scores
        
        return scores
    
    def _get_match_reasons(self, job: pd.Series, user_profile: Dict[str, Any]) -> List[str]:
        """Get reasons why a job matches the user"""
        reasons = []
        
        # Skill matches
        user_skills = set(user_profile.get('skills', []))
        job_skills = set(job['extracted_skills'])
        matching_skills = user_skills.intersection(job_skills)
        
        if matching_skills:
            reasons.append(f"Skills match: {', '.join(list(matching_skills)[:3])}")
        
        # Experience level match
        if job['complexity_score'] < 0.4:
            reasons.append("Suitable for beginners")
        elif job['complexity_score'] > 0.7:
            reasons.append("Advanced role - good for growth")
        
        # Location match
        if job['is_remote'] and user_profile.get('location_preference') == 'remote':
            reasons.append("Remote position matches preference")
        
        # High similarity score
        if job['user_similarity'] > 0.7:
            reasons.append("High profile similarity")
        
        return reasons
    
    def get_similar_jobs(self, job_id: int, n_similar: int = 5) -> List[Dict]:
        """Get similar jobs based on content similarity"""
        if self.similarity_matrix is None:
            return []
        
        # Get similarity scores for the job
        job_similarities = self.similarity_matrix[job_id]
        
        # Get top similar jobs (excluding itself)
        similar_indices = np.argsort(job_similarities)[::-1][1:n_similar+1]
        
        similar_jobs = []
        for idx in similar_indices:
            job_dict = self.jobs_df.iloc[idx].to_dict()
            job_dict['similarity_score'] = job_similarities[idx]
            similar_jobs.append(job_dict)
        
        return similar_jobs
    
    def get_job_insights(self) -> Dict[str, Any]:
        """Get insights about the job market"""
        insights = {
            'total_jobs': len(self.jobs_df),
            'remote_jobs_percentage': (self.jobs_df['is_remote'].sum() / len(self.jobs_df)) * 100,
            'average_salary': self.jobs_df['salary_numeric'].mean(),
            'top_skills': self._get_top_skills(),
            'cluster_distribution': self.jobs_df['cluster'].value_counts().to_dict(),
            'topic_distribution': self.jobs_df['topic'].value_counts().to_dict(),
            'complexity_distribution': {
                'beginner': (self.jobs_df['complexity_score'] < 0.3).sum(),
                'intermediate': ((self.jobs_df['complexity_score'] >= 0.3) & 
                               (self.jobs_df['complexity_score'] < 0.7)).sum(),
                'advanced': (self.jobs_df['complexity_score'] >= 0.7).sum()
            }
        }
        
        return insights
    
    def _get_top_skills(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """Get most common skills in job market"""
        all_skills = []
        for skills in self.jobs_df['extracted_skills']:
            all_skills.extend(skills)
        
        skill_counts = pd.Series(all_skills).value_counts()
        return list(skill_counts.head(top_n).items())
    
    def save_model(self, filepath: str = 'recommendation_model.pkl'):
        """Save the recommendation model"""
        model_data = {
            'vectorizer': self.vectorizer,
            'clustering_model': self.clustering_model,
            'topic_model': self.topic_model,
            'scaler': self.scaler,
            'skill_weights': self.skill_weights
        }
        joblib.dump(model_data, filepath)
        self.logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str = 'recommendation_model.pkl'):
        """Load the recommendation model"""
        model_data = joblib.load(filepath)
        self.vectorizer = model_data['vectorizer']
        self.clustering_model = model_data['clustering_model']
        self.topic_model = model_data['topic_model']
        self.scaler = model_data['scaler']
        self.skill_weights = model_data['skill_weights']
        self.logger.info(f"Model loaded from {filepath}")

# Example usage
if __name__ == "__main__":
    # Initialize recommendation system
    recommender = MLRecommendationSystem()
    
    # Example job data
    sample_jobs = [
        {
            'title': 'Machine Learning Intern',
            'company': 'TechCorp AI',
            'description': 'Python, TensorFlow, machine learning, deep learning',
            'location': 'Remote',
            'salary': '$25-35/hour'
        },
        {
            'title': 'Data Science Intern',
            'company': 'Analytics Pro',
            'description': 'Python, pandas, scikit-learn, statistics',
            'location': 'San Francisco',
            'salary': '$30-40/hour'
        }
    ]
    
    # Build model
    recommender.build_recommendation_model(sample_jobs)
    
    # Example user profile
    user_profile = {
        'name': 'John Doe',
        'skills': ['python', 'machine learning', 'tensorflow'],
        'experience_level': 'intermediate',
        'location_preference': 'remote'
    }
    
    # Get recommendations
    recommendations = recommender.get_personalized_recommendations(user_profile)
    print(f"Found {len(recommendations)} recommendations") 