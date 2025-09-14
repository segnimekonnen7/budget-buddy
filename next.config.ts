import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Explicitly set the root directory
  experimental: {
    turbo: {
      root: __dirname,
    },
  },
  // Disable workspace inference
  typescript: {
    ignoreBuildErrors: false,
  },
};

export default nextConfig;
