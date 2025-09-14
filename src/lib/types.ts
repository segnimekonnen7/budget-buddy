export type JobSource = "greenhouse" | "lever" | "workday" | "usajobs" | "yc_rss" | "serpapi" | "custom_rss" | "other";
export type JobType = "Internship" | "Co-op" | "Full-time" | "Part-time";
export type ApplicationStatus = "Interested" | "Applied" | "OA" | "Interview" | "Offer" | "Rejected";
export type AlertFrequency = "none" | "daily" | "weekly";

export interface NormalizedJob {
  id: string;               // stable hash (source + externalId + company + title)
  source: JobSource;
  externalId?: string;
  title: string;
  company: string;
  location: string;         // "City, State" or "Remote"
  jobType?: JobType;
  postedAt?: string;        // ISO
  applyUrl: string;
  descriptionSnippet?: string;
  raw?: unknown;            // keep minimal raw payload
  majorTags: string[];      // normalized tags derived from title/desc (e.g., ["CIT","Networking"])
  keywords: string[];       // extracted from desc/title
}

export interface SourceAdapter {
  name: string;
  enabled: boolean;
  fetchJobs(params: { query: string; location?: string; majors?: string[]; }): Promise<NormalizedJob[]>;
}

export interface SearchParams {
  query?: string;
  location?: string;
  majors?: string[];
  jobType?: JobType;
  page?: number;
  limit?: number;
}

export interface SearchResponse {
  items: NormalizedJob[];
  nextCursor?: string;
  stats: {
    total: number;
    deduped: number;
  };
}

export interface SavedSearch {
  id: string;
  userId: string;
  name: string;
  query: string;
  majors: string[];
  location?: string;
  alertFreq: AlertFrequency;
  lastRunAt?: Date;
}

export interface Application {
  id: string;
  userId: string;
  jobId: string;
  status: ApplicationStatus;
  notes?: string;
  updatedAt: Date;
  createdAt: Date;
  job?: NormalizedJob;
}

export interface Bookmark {
  id: string;
  userId: string;
  jobId: string;
  job?: NormalizedJob;
}

export interface IngestLog {
  id: string;
  adapter: string;
  runId: string;
  count: number;
  errors: number;
  startedAt: Date;
  finishedAt?: Date;
  notes?: string;
}

// API Response types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  nextCursor?: string;
  hasMore: boolean;
  total: number;
}

// Form schemas
export interface SearchFormData {
  query: string;
  location: string;
  majors: string[];
  jobType?: JobType;
}

export interface SavedSearchFormData {
  name: string;
  query: string;
  majors: string[];
  location?: string;
  alertFreq: AlertFrequency;
}

export interface ApplicationFormData {
  status: ApplicationStatus;
  notes?: string;
}
