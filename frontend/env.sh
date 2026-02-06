#!/bin/sh
# Script to handle environment variables for frontend container

# Create a JavaScript file with environment variables
cat > /usr/share/nginx/html/_next/static/env-config.js << EOF
window.env = {
  NEXT_PUBLIC_API_URL: '${NEXT_PUBLIC_API_URL:-http://localhost:8000}'
};
EOF

# Start nginx without daemon mode and without pid file
exec nginx -g "daemon off; pid /tmp/nginx.pid;"