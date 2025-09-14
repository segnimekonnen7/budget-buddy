import { SourceAdapter, NormalizedJob } from '@/lib/types';
import { GreenhouseAdapter } from './greenhouse-adapter';
import { LeverAdapter } from './lever-adapter';
import { YCRSSAdapter } from './yc-rss-adapter';

// Import disabled adapters with clear ToS notices
// LinkedIn/Glassdoor adapters are intentionally disabled due to ToS violations
// They will be enabled only when compliant API access is provided

export class AdapterManager {
  private adapters: Map<string, SourceAdapter> = new Map();

  constructor() {
    // Initialize enabled adapters
    this.registerAdapter(new GreenhouseAdapter());
    this.registerAdapter(new LeverAdapter());
    this.registerAdapter(new YCRSSAdapter());
    
    // TODO: Add more adapters as they become available
    // this.registerAdapter(new WorkdayAdapter());
    // this.registerAdapter(new USAJobsAdapter());
    // this.registerAdapter(new SerpAPIAdapter());
  }

  private registerAdapter(adapter: SourceAdapter): void {
    this.adapters.set(adapter.name, adapter);
  }

  getAdapter(name: string): SourceAdapter | undefined {
    return this.adapters.get(name);
  }

  getAllAdapters(): SourceAdapter[] {
    return Array.from(this.adapters.values());
  }

  getEnabledAdapters(): SourceAdapter[] {
    return this.getAllAdapters().filter(adapter => adapter.enabled);
  }

  async fetchJobsFromAllSources(params: { 
    query: string; 
    location?: string; 
    majors?: string[]; 
  }): Promise<NormalizedJob[]> {
    const enabledAdapters = this.getEnabledAdapters();
    const allJobs: NormalizedJob[] = [];

    // Fetch jobs from all enabled adapters in parallel
    const promises = enabledAdapters.map(async (adapter) => {
      try {
        console.log(`Fetching jobs from ${adapter.name}...`);
        const jobs = await adapter.fetchJobs(params);
        console.log(`Found ${jobs.length} jobs from ${adapter.name}`);
        return jobs;
      } catch (error) {
        console.error(`Error fetching from ${adapter.name}:`, error);
        return [];
      }
    });

    const results = await Promise.allSettled(promises);
    
    for (const result of results) {
      if (result.status === 'fulfilled') {
        allJobs.push(...result.value);
      }
    }

    return allJobs;
  }

  async fetchJobsFromSource(
    sourceName: string, 
    params: { query: string; location?: string; majors?: string[]; }
  ): Promise<NormalizedJob[]> {
    const adapter = this.getAdapter(sourceName);
    if (!adapter) {
      throw new Error(`Adapter '${sourceName}' not found`);
    }
    
    if (!adapter.enabled) {
      throw new Error(`Adapter '${sourceName}' is disabled`);
    }

    return adapter.fetchJobs(params);
  }

  // Admin functions
  enableAdapter(name: string): boolean {
    const adapter = this.getAdapter(name);
    if (adapter) {
      (adapter as any).enabled = true;
      return true;
    }
    return false;
  }

  disableAdapter(name: string): boolean {
    const adapter = this.getAdapter(name);
    if (adapter) {
      (adapter as any).enabled = false;
      return true;
    }
    return false;
  }

  getAdapterStatus(): Array<{ name: string; enabled: boolean }> {
    return this.getAllAdapters().map(adapter => ({
      name: adapter.name,
      enabled: adapter.enabled
    }));
  }
}

// Export singleton instance
export const adapterManager = new AdapterManager();

// Export individual adapters for testing
export { GreenhouseAdapter, LeverAdapter, YCRSSAdapter };
