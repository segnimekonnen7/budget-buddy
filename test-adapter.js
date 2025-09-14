// Simple test script to verify adapters work
const { adapterManager } = require('./src/lib/adapters/index.ts');

async function testAdapters() {
  console.log('🧪 Testing Internship Finder Adapters...\n');
  
  try {
    // Test adapter status
    const adapters = adapterManager.getAdapterStatus();
    console.log('📊 Adapter Status:');
    adapters.forEach(adapter => {
      console.log(`  ${adapter.enabled ? '✅' : '❌'} ${adapter.name}`);
    });
    
    console.log('\n🔍 Testing job fetching...');
    
    // Test fetching jobs
    const jobs = await adapterManager.fetchJobsFromAllSources({
      query: 'software',
      location: 'remote',
      majors: ['CS', 'SWE']
    });
    
    console.log(`\n📈 Results:`);
    console.log(`  Total jobs found: ${jobs.length}`);
    
    if (jobs.length > 0) {
      console.log('\n📋 Sample jobs:');
      jobs.slice(0, 3).forEach((job, index) => {
        console.log(`  ${index + 1}. ${job.title} at ${job.company}`);
        console.log(`     Location: ${job.location}`);
        console.log(`     Source: ${job.source}`);
        console.log(`     Apply: ${job.applyUrl}`);
        console.log('');
      });
    }
    
    console.log('✅ Test completed successfully!');
    
  } catch (error) {
    console.error('❌ Test failed:', error);
  }
}

testAdapters();
