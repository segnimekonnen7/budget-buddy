import { BaseAdapter } from './base-adapter';
import { NormalizedJob } from '@/lib/types';

interface LeverJob {
  id: string;
  text: string;
  hostedUrl: string;
  applyUrl: string;
  categories: {
    location: string;
    team: string;
    commitment: string;
  };
  createdAt: number;
  descriptionPlain: string;
}

interface LeverResponse {
  data: LeverJob[];
}

export class LeverAdapter extends BaseAdapter {
  name = 'lever';
  enabled = true;

  async fetchJobs(params: { query: string; location?: string; majors?: string[]; }): Promise<NormalizedJob[]> {
    try {
      const jobs: NormalizedJob[] = [];
      
      // Lever public job boards - popular companies
      const companies = [
        'uber',
        'lyft',
        'square',
        'dropbox',
        'slack',
        'zoom',
        'pinterest',
        'snapchat'
      ];

      for (const company of companies) {
        try {
          const response = await this.retry(async () => {
            const res = await fetch(`https://api.lever.co/v0/postings/${company}?mode=json`);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return res.json() as Promise<LeverResponse>;
          });

          const filteredJobs = response.data.filter(job => {
            // Filter for internships
            const isInternship = job.text.toLowerCase().includes('intern') || 
                               job.text.toLowerCase().includes('internship') ||
                               job.categories.team.toLowerCase().includes('intern') ||
                               job.categories.commitment.toLowerCase().includes('intern');
            
            // Filter by query if provided
            const matchesQuery = !params.query || 
                               job.text.toLowerCase().includes(params.query.toLowerCase()) ||
                               job.categories.team.toLowerCase().includes(params.query.toLowerCase()) ||
                               job.descriptionPlain.toLowerCase().includes(params.query.toLowerCase());
            
            // Filter by location if provided
            const matchesLocation = !params.location || 
                                  job.categories.location.toLowerCase().includes(params.location.toLowerCase()) ||
                                  job.categories.location.toLowerCase().includes('remote') ||
                                  job.categories.location.toLowerCase().includes('anywhere');

            return isInternship && matchesQuery && matchesLocation;
          });

          for (const job of filteredJobs) {
            const normalizedJob = this.normalizeJob(
              this.name,
              job.id,
              job.text,
              company.charAt(0).toUpperCase() + company.slice(1), // Capitalize company name
              job.categories.location,
              job.applyUrl,
              job.descriptionPlain,
              'Internship',
              new Date(job.createdAt).toISOString()
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
}
