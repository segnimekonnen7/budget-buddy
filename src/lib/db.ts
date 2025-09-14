import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma = globalForPrisma.prisma ?? new PrismaClient();

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;

// Helper function to create stable job ID
export function createJobId(source: string, externalId: string, company: string, title: string): string {
  const data = `${source}|${externalId}|${company}|${title}`;
  return require('crypto').createHash('sha256').update(data).digest('hex');
}

// Helper function to normalize location
export function normalizeLocation(location: string): string {
  if (!location) return 'Remote';
  
  const normalized = location.trim();
  if (normalized.toLowerCase().includes('remote') || normalized.toLowerCase().includes('anywhere')) {
    return 'Remote';
  }
  
  return normalized;
}

// Helper function to extract keywords from text
export function extractKeywords(text: string): string[] {
  if (!text) return [];
  
  // Simple keyword extraction - in production, you might want to use NLP libraries
  const words = text.toLowerCase()
    .replace(/[^\w\s]/g, ' ')
    .split(/\s+/)
    .filter(word => word.length > 2)
    .filter(word => !['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'].includes(word));
  
  return [...new Set(words)].slice(0, 20); // Limit to 20 unique keywords
}

// Helper function to extract major tags
export function extractMajorTags(title: string, description: string): string[] {
  const majors = [
    'CIT', 'CS', 'SWE', 'Data', 'Security', 'Networking', 'Cybersecurity',
    'Computer Science', 'Software Engineering', 'Information Technology',
    'Data Science', 'Machine Learning', 'AI', 'Artificial Intelligence',
    'Web Development', 'Mobile Development', 'DevOps', 'Cloud Computing'
  ];
  
  const text = `${title} ${description}`.toLowerCase();
  const foundMajors = majors.filter(major => 
    text.includes(major.toLowerCase()) || text.includes(major.replace(' ', '').toLowerCase())
  );
  
  return foundMajors;
}

// Helper function to calculate match score
export function calculateMatchScore(jobKeywords: string[], userKeywords: string[]): number {
  if (!userKeywords.length || !jobKeywords.length) return 0;
  
  const userSet = new Set(userKeywords.map(k => k.toLowerCase()));
  const jobSet = new Set(jobKeywords.map(k => k.toLowerCase()));
  
  const intersection = new Set([...userSet].filter(x => jobSet.has(x)));
  const union = new Set([...userSet, ...jobSet]);
  
  return intersection.size / union.size; // Jaccard similarity
}

// Helper function to calculate recency boost
export function calculateRecencyBoost(postedAt: Date): number {
  const now = new Date();
  const daysSincePosted = Math.floor((now.getTime() - postedAt.getTime()) / (1000 * 60 * 60 * 24));
  
  // Exponential decay: newer posts get higher scores
  return Math.exp(-daysSincePosted / 30); // Decay over 30 days
}

// Helper function to calculate ranking score
export function calculateRankingScore(
  textMatch: number,
  recencyBoost: number,
  companySignal: number = 0.5 // Default neutral score
): number {
  return 0.6 * textMatch + 0.3 * recencyBoost + 0.1 * companySignal;
}
