import { NextResponse } from 'next/server';
import { adapterManager } from '@/lib/adapters';

export async function GET() {
  try {
    const adapters = adapterManager.getAdapterStatus();
    
    return NextResponse.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      version: '1.0.0',
      adapters: adapters,
      endpoints: {
        jobs: '/api/jobs',
        health: '/api/health'
      }
    });
  } catch (error) {
    return NextResponse.json(
      { 
        status: 'error', 
        error: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString()
      },
      { status: 500 }
    );
  }
}
