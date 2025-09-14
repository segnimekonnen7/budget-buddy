import { NormalizedJob, SearchParams } from '@/lib/types';
import { calculateMatchScore, calculateRecencyBoost, calculateRankingScore } from '@/lib/db';

export interface RankedJob extends NormalizedJob {
  rankingScore: number;
  matchScore: number;
  recencyBoost: number;
  companySignal: number;
}

export interface DeduplicationResult {
  jobs: RankedJob[];
  stats: {
    total: number;
    deduped: number;
    duplicates: number;
  };
}

// Curated list of top companies for company signal boost
const TOP_COMPANIES = new Set([
  'google', 'microsoft', 'apple', 'amazon', 'meta', 'netflix', 'airbnb', 'uber',
  'stripe', 'discord', 'robinhood', 'coinbase', 'figma', 'notion', 'linear',
  'openai', 'anthropic', 'databricks', 'snowflake', 'palantir', 'tesla', 'spacex'
]);

export function deduplicateJobs(jobs: NormalizedJob[]): DeduplicationResult {
  const jobMap = new Map<string, NormalizedJob>();
  const duplicates = new Set<string>();

  for (const job of jobs) {
    const key = createDeduplicationKey(job);
    
    if (jobMap.has(key)) {
      // Keep the more recent job if there's a duplicate
      const existing = jobMap.get(key)!;
      const existingDate = existing.postedAt ? new Date(existing.postedAt) : new Date(0);
      const newDate = job.postedAt ? new Date(job.postedAt) : new Date(0);
      
      if (newDate > existingDate) {
        jobMap.set(key, job);
      }
      duplicates.add(key);
    } else {
      jobMap.set(key, job);
    }
  }

  const dedupedJobs = Array.from(jobMap.values());

  return {
    jobs: dedupedJobs,
    stats: {
      total: jobs.length,
      deduped: dedupedJobs.length,
      duplicates: duplicates.size
    }
  };
}

export function rankJobs(
  jobs: NormalizedJob[], 
  searchParams: SearchParams,
  userKeywords: string[] = []
): RankedJob[] {
  const rankedJobs: RankedJob[] = [];

  for (const job of jobs) {
    // Calculate match score based on search query and user keywords
    const queryKeywords = searchParams.query ? searchParams.query.toLowerCase().split(/\s+/) : [];
    const allKeywords = [...queryKeywords, ...userKeywords];
    
    const matchScore = calculateMatchScore(job.keywords, allKeywords);
    
    // Calculate recency boost
    const recencyBoost = job.postedAt ? calculateRecencyBoost(new Date(job.postedAt)) : 0.5;
    
    // Calculate company signal
    const companySignal = calculateCompanySignal(job.company);
    
    // Calculate overall ranking score
    const rankingScore = calculateRankingScore(matchScore, recencyBoost, companySignal);
    
    rankedJobs.push({
      ...job,
      rankingScore,
      matchScore,
      recencyBoost,
      companySignal
    });
  }

  // Sort by ranking score (highest first)
  return rankedJobs.sort((a, b) => b.rankingScore - a.rankingScore);
}

export function filterJobs(
  jobs: RankedJob[],
  searchParams: SearchParams
): RankedJob[] {
  return jobs.filter(job => {
    // Filter by job type
    if (searchParams.jobType && job.jobType !== searchParams.jobType) {
      return false;
    }
    
    // Filter by majors if specified
    if (searchParams.majors && searchParams.majors.length > 0) {
      const jobMajors = job.majorTags.map(tag => tag.toLowerCase());
      const searchMajors = searchParams.majors.map(major => major.toLowerCase());
      const hasMatchingMajor = searchMajors.some(major => 
        jobMajors.some(jobMajor => jobMajor.includes(major) || major.includes(jobMajor))
      );
      
      if (!hasMatchingMajor) {
        return false;
      }
    }
    
    return true;
  });
}

export function paginateJobs(
  jobs: RankedJob[],
  page: number = 1,
  limit: number = 20
): { jobs: RankedJob[]; hasMore: boolean; total: number } {
  const startIndex = (page - 1) * limit;
  const endIndex = startIndex + limit;
  
  return {
    jobs: jobs.slice(startIndex, endIndex),
    hasMore: endIndex < jobs.length,
    total: jobs.length
  };
}

function createDeduplicationKey(job: NormalizedJob): string {
  // Create a stable key for deduplication
  const company = job.company.toLowerCase().trim();
  const title = job.title.toLowerCase().trim();
  const location = job.location.toLowerCase().trim();
  const normalizedUrl = normalizeUrl(job.applyUrl);
  
  // Get week of year for recency window dedup
  const week = job.postedAt ? getWeekOfYear(new Date(job.postedAt)) : 'unknown';
  
  return `${company}|${title}|${location}|${normalizedUrl}|${week}`;
}

function normalizeUrl(url: string): string {
  try {
    const urlObj = new URL(url);
    // Remove query parameters and fragments for deduplication
    return `${urlObj.protocol}//${urlObj.host}${urlObj.pathname}`;
  } catch {
    return url;
  }
}

function getWeekOfYear(date: Date): string {
  const startOfYear = new Date(date.getFullYear(), 0, 1);
  const days = Math.floor((date.getTime() - startOfYear.getTime()) / (24 * 60 * 60 * 1000));
  const weekNumber = Math.ceil(days / 7);
  return `${date.getFullYear()}-W${weekNumber.toString().padStart(2, '0')}`;
}

function calculateCompanySignal(company: string): number {
  const companyLower = company.toLowerCase();
  
  // Check if it's in our curated top companies list
  if (TOP_COMPANIES.has(companyLower)) {
    return 1.0; // Maximum signal for top companies
  }
  
  // Check for common patterns that indicate established companies
  if (companyLower.includes('inc') || companyLower.includes('corp') || companyLower.includes('llc')) {
    return 0.8;
  }
  
  // Default neutral signal
  return 0.5;
}

// Full-text search helper (for PostgreSQL FTS)
export function createSearchQuery(searchParams: SearchParams): string {
  const terms: string[] = [];
  
  if (searchParams.query) {
    terms.push(searchParams.query);
  }
  
  if (searchParams.majors) {
    terms.push(...searchParams.majors);
  }
  
  if (searchParams.location && searchParams.location !== 'Remote') {
    terms.push(searchParams.location);
  }
  
  return terms.join(' & ');
}
