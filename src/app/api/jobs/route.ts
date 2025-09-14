import { NextRequest, NextResponse } from 'next/server';
import { adapterManager } from '@/lib/adapters';
import { deduplicateJobs, rankJobs, filterJobs, paginateJobs } from '@/lib/ranking';
import { SearchParams, SearchResponse } from '@/lib/types';
import { prisma } from '@/lib/db';

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    
    // Parse search parameters
    const params: SearchParams = {
      query: searchParams.get('query') || undefined,
      location: searchParams.get('location') || undefined,
      majors: searchParams.get('majors')?.split(',').filter(Boolean) || undefined,
      jobType: searchParams.get('jobType') as any || undefined,
      page: parseInt(searchParams.get('page') || '1'),
      limit: parseInt(searchParams.get('limit') || '20')
    };

    console.log('Search params:', params);

    // Fetch jobs from all enabled sources
    const rawJobs = await adapterManager.fetchJobsFromAllSources({
      query: params.query || '',
      location: params.location,
      majors: params.majors
    });

    console.log(`Fetched ${rawJobs.length} raw jobs`);

    // Deduplicate jobs
    const dedupResult = deduplicateJobs(rawJobs);
    console.log(`Deduplicated: ${dedupResult.stats.total} -> ${dedupResult.stats.deduped}`);

    // Rank jobs
    const rankedJobs = rankJobs(dedupResult.jobs, params);
    console.log(`Ranked ${rankedJobs.length} jobs`);

    // Filter jobs
    const filteredJobs = filterJobs(rankedJobs, params);
    console.log(`Filtered to ${filteredJobs.length} jobs`);

    // Paginate results
    const paginatedResult = paginateJobs(
      filteredJobs, 
      params.page, 
      Math.min(params.limit, 50) // Cap at 50 per page
    );

    // Store jobs in database for caching and analytics
    await storeJobsInDatabase(dedupResult.jobs);

    const response: SearchResponse = {
      items: paginatedResult.jobs.map(job => ({
        id: job.id,
        source: job.source,
        externalId: job.externalId,
        title: job.title,
        company: job.company,
        location: job.location,
        jobType: job.jobType,
        postedAt: job.postedAt,
        applyUrl: job.applyUrl,
        descriptionSnippet: job.descriptionSnippet,
        majorTags: job.majorTags,
        keywords: job.keywords
      })),
      nextCursor: paginatedResult.hasMore ? (params.page + 1).toString() : undefined,
      stats: {
        total: dedupResult.stats.total,
        deduped: paginatedResult.total
      }
    };

    return NextResponse.json(response);
  } catch (error) {
    console.error('Error in jobs API:', error);
    return NextResponse.json(
      { error: 'Failed to fetch jobs' },
      { status: 500 }
    );
  }
}

async function storeJobsInDatabase(jobs: any[]) {
  try {
    // Store jobs in batches to avoid overwhelming the database
    const batchSize = 50;
    for (let i = 0; i < jobs.length; i += batchSize) {
      const batch = jobs.slice(i, i + batchSize);
      
      await Promise.allSettled(
        batch.map(async (job) => {
          try {
            await prisma.job.upsert({
              where: { id: job.id },
              update: {
                title: job.title,
                company: job.company,
                location: job.location,
                jobType: job.jobType,
                postedAt: job.postedAt ? new Date(job.postedAt) : null,
                applyUrl: job.applyUrl,
                descriptionSnippet: job.descriptionSnippet,
                majorTags: JSON.stringify(job.majorTags),
                keywords: JSON.stringify(job.keywords),
                updatedAt: new Date()
              },
              create: {
                id: job.id,
                source: job.source,
                externalId: job.externalId,
                title: job.title,
                company: job.company,
                location: job.location,
                jobType: job.jobType,
                postedAt: job.postedAt ? new Date(job.postedAt) : null,
                applyUrl: job.applyUrl,
                descriptionSnippet: job.descriptionSnippet,
                majorTags: JSON.stringify(job.majorTags),
                keywords: JSON.stringify(job.keywords)
              }
            });
          } catch (error) {
            console.error(`Error storing job ${job.id}:`, error);
          }
        })
      );
    }
  } catch (error) {
    console.error('Error storing jobs in database:', error);
  }
}
