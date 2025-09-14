import { SourceAdapter, NormalizedJob } from '@/lib/types';
import { createJobId, normalizeLocation, extractKeywords, extractMajorTags } from '@/lib/db';

export abstract class BaseAdapter implements SourceAdapter {
  abstract name: string;
  abstract enabled: boolean;

  abstract fetchJobs(params: { 
    query: string; 
    location?: string; 
    majors?: string[]; 
  }): Promise<NormalizedJob[]>;

  // Common normalization method
  protected normalizeJob(
    source: string,
    externalId: string,
    title: string,
    company: string,
    location: string,
    applyUrl: string,
    description?: string,
    jobType?: string,
    postedAt?: string
  ): NormalizedJob {
    const normalizedLocation = normalizeLocation(location);
    const keywords = extractKeywords(`${title} ${description || ''}`);
    const majorTags = extractMajorTags(title, description || '');
    
    return {
      id: createJobId(source, externalId, company, title),
      source: source as any,
      externalId,
      title: title.trim(),
      company: company.trim(),
      location: normalizedLocation,
      jobType: jobType as any,
      postedAt,
      applyUrl,
      descriptionSnippet: description?.substring(0, 200) + (description && description.length > 200 ? '...' : ''),
      majorTags,
      keywords,
      raw: { source, externalId, originalLocation: location }
    };
  }

  // Common error handling
  protected handleError(error: any, context: string): NormalizedJob[] {
    console.error(`Error in ${this.name} adapter (${context}):`, error);
    return [];
  }

  // Rate limiting helper
  protected async delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Retry helper
  protected async retry<T>(
    fn: () => Promise<T>,
    maxRetries: number = 3,
    delayMs: number = 1000
  ): Promise<T> {
    for (let i = 0; i < maxRetries; i++) {
      try {
        return await fn();
      } catch (error) {
        if (i === maxRetries - 1) throw error;
        await this.delay(delayMs * Math.pow(2, i)); // Exponential backoff
      }
    }
    throw new Error('Max retries exceeded');
  }
}
