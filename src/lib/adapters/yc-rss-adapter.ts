import { BaseAdapter } from './base-adapter';
import { NormalizedJob } from '@/lib/types';

interface RSSItem {
  title: string;
  link: string;
  description: string;
  pubDate: string;
  guid: string;
}

interface RSSResponse {
  rss: {
    channel: {
      item: RSSItem[];
    };
  };
}

export class YCRSSAdapter extends BaseAdapter {
  name = 'yc_rss';
  enabled = true;

  async fetchJobs(params: { query: string; location?: string; majors?: string[]; }): Promise<NormalizedJob[]> {
    try {
      const response = await this.retry(async () => {
        const res = await fetch('https://news.ycombinator.com/jobs.rss');
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const text = await res.text();
        
        // Simple XML parsing - in production, use a proper XML parser
        return this.parseRSS(text);
      });

      const jobs: NormalizedJob[] = [];

      for (const item of response.rss.channel.item) {
        // Filter for internships
        const isInternship = item.title.toLowerCase().includes('intern') || 
                           item.title.toLowerCase().includes('internship') ||
                           item.description.toLowerCase().includes('intern') ||
                           item.description.toLowerCase().includes('internship');
        
        // Filter by query if provided
        const matchesQuery = !params.query || 
                           item.title.toLowerCase().includes(params.query.toLowerCase()) ||
                           item.description.toLowerCase().includes(params.query.toLowerCase());
        
        // Filter by location if provided
        const matchesLocation = !params.location || 
                              item.title.toLowerCase().includes(params.location.toLowerCase()) ||
                              item.description.toLowerCase().includes(params.location.toLowerCase()) ||
                              item.title.toLowerCase().includes('remote') ||
                              item.description.toLowerCase().includes('remote');

        if (isInternship && matchesQuery && matchesLocation) {
          const company = this.extractCompany(item.title);
          const location = this.extractLocation(item.title, item.description);
          
          const normalizedJob = this.normalizeJob(
            this.name,
            item.guid,
            item.title,
            company,
            location,
            item.link,
            item.description,
            'Internship',
            item.pubDate
          );
          
          jobs.push(normalizedJob);
        }
      }

      return jobs;
    } catch (error) {
      return this.handleError(error, 'fetchJobs');
    }
  }

  private parseRSS(xmlText: string): RSSResponse {
    // Simple XML parsing - in production, use a proper XML parser like xml2js
    const items: RSSItem[] = [];
    
    // Extract items using regex (simplified)
    const itemRegex = /<item>([\s\S]*?)<\/item>/g;
    let match;
    
    while ((match = itemRegex.exec(xmlText)) !== null) {
      const itemXml = match[1];
      
      const title = this.extractTag(itemXml, 'title');
      const link = this.extractTag(itemXml, 'link');
      const description = this.extractTag(itemXml, 'description');
      const pubDate = this.extractTag(itemXml, 'pubDate');
      const guid = this.extractTag(itemXml, 'guid');
      
      if (title && link) {
        items.push({
          title: this.decodeHtml(title),
          link: this.decodeHtml(link),
          description: this.decodeHtml(description),
          pubDate,
          guid: this.decodeHtml(guid) || link
        });
      }
    }
    
    return {
      rss: {
        channel: {
          item: items
        }
      }
    };
  }

  private extractTag(xml: string, tag: string): string {
    const regex = new RegExp(`<${tag}[^>]*>([\\s\\S]*?)<\\/${tag}>`, 'i');
    const match = xml.match(regex);
    return match ? match[1].trim() : '';
  }

  private decodeHtml(html: string): string {
    return html
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/&quot;/g, '"')
      .replace(/&#39;/g, "'")
      .replace(/&nbsp;/g, ' ');
  }

  private extractCompany(title: string): string {
    // Extract company name from title (usually in format "Company Name is hiring...")
    const match = title.match(/^([^,]+)/);
    return match ? match[1].trim() : 'Unknown Company';
  }

  private extractLocation(title: string, description: string): string {
    // Try to extract location from title or description
    const locationPatterns = [
      /in\s+([^,]+)/i,
      /at\s+([^,]+)/i,
      /location[:\s]+([^,\n]+)/i,
      /based\s+in\s+([^,\n]+)/i
    ];
    
    const text = `${title} ${description}`;
    
    for (const pattern of locationPatterns) {
      const match = text.match(pattern);
      if (match) {
        const location = match[1].trim();
        if (location.length > 0 && location.length < 50) {
          return location;
        }
      }
    }
    
    return 'Remote'; // Default to remote if no location found
  }
}
