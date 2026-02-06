/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export', // This will create an 'out' directory instead of .next
  trailingSlash: true, // Ensure all routes have trailing slashes for compatibility
  images: {
    unoptimized: true // Required for export
  }
};

module.exports = nextConfig;