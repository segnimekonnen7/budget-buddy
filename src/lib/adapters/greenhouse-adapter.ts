import { BaseAdapter } from './base-adapter';
import { NormalizedJob } from '@/lib/types';

interface GreenhouseJob {
  id: number;
  title: string;
  location: {
    name: string;
  };
  absolute_url: string;
  departments: Array<{
    name: string;
  }>;
  metadata: Array<{
    id: number;
    name: string;
    value_type: string;
    value: string;
  }>;
  updated_at: string;
}

interface GreenhouseResponse {
  jobs: GreenhouseJob[];
}

export class GreenhouseAdapter extends BaseAdapter {
  name = 'greenhouse';
  enabled = true;

  async fetchJobs(params: { query: string; location?: string; majors?: string[]; }): Promise<NormalizedJob[]> {
    try {
      const jobs: NormalizedJob[] = [];
      
      // Greenhouse public job boards - we'll use a few popular companies
      const companies = [
        'airbnb',
        'stripe',
        'discord',
        'robinhood',
        'coinbase',
        'figma',
        'notion',
        'linear'
      ];

      for (const company of companies) {
        try {
          const response = await this.retry(async () => {
            const res = await fetch(`https://boards-api.greenhouse.io/v1/boards/${company}/jobs`);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return res.json() as Promise<GreenhouseResponse>;
          });

          const filteredJobs = response.jobs.filter(job => {
            // Filter for internships
            const isInternship = job.title.toLowerCase().includes('intern') || 
                               job.title.toLowerCase().includes('internship') ||
                               job.departments.some(dept => dept.name.toLowerCase().includes('intern'));
            
            // Filter by query if provided
            const matchesQuery = !params.query || 
                               job.title.toLowerCase().includes(params.query.toLowerCase()) ||
                               job.departments.some(dept => dept.name.toLowerCase().includes(params.query.toLowerCase()));
            
            // Filter by location if provided
            const matchesLocation = !params.location || 
                                  job.location.name.toLowerCase().includes(params.location.toLowerCase()) ||
                                  job.location.name.toLowerCase().includes('remote');

            return isInternship && matchesQuery && matchesLocation;
          });

          for (const job of filteredJobs) {
            const normalizedJob = this.normalizeJob(
              this.name,
              job.id.toString(),
              job.title,
              company.charAt(0).toUpperCase() + company.slice(1), // Capitalize company name
              job.location.name,
              job.absolute_url,
              this.extractDescription(job),
              'Internship',
              job.updated_at
            );
            
            jobs.push(normalizedJob);
          }

          // Rate limiting
          await this.delay(100);
        } catch (error) {
          console.error(`Error fetching from ${company}:`, error);
          continue;
        }
      }

      return jobs;
    } catch (error) {
      return this.handleError(error, 'fetchJobs');
    }
  }

  private extractDescription(job: GreenhouseJob): string {
    // Try to extract description from metadata
    const descriptionMeta = job.metadata.find(meta => 
      meta.name.toLowerCase().includes('description') || 
      meta.name.toLowerCase().includes('summary')
    );
    
    if (descriptionMeta?.value) {
      return descriptionMeta.value;
    }

    // Fallback to department names
    return job.departments.map(dept => dept.name).join(', ');
  }
}
