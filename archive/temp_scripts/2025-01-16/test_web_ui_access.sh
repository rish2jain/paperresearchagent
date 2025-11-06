#!/bin/bash
# Test Web UI accessibility via LoadBalancer
# Usage: WEB_UI_URL=http://... API_URL=http://... ./test_web_ui_access.sh

# Default URLs (can be overridden via environment variables)
WEB_UI_URL="${WEB_UI_URL:-http://a5e4e8ba7d0454a8e85a1c1c7d35b9b1-1577638137.us-east-2.elb.amazonaws.com:8501}"
API_URL="${API_URL:-http://a80d619b6d4494eb59d1f6dd5af5ee00-731672944.us-east-2.elb.amazonaws.com:8080}"

echo "=== Testing Web UI Access ==="
echo "URL: $WEB_UI_URL"
echo ""

# Test health endpoint
echo "1. Testing health endpoint..."
curl -s --max-time 10 "$WEB_UI_URL/_stcore/health" && echo " ✅" || echo " ❌"
echo ""

# Test main page
echo "2. Testing main page..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 15 "$WEB_UI_URL")
if [ "$HTTP_CODE" = "200" ]; then
    echo "   HTTP Status: $HTTP_CODE ✅"
else
    echo "   HTTP Status: $HTTP_CODE ❌"
fi
echo ""

# Test API endpoint
echo "3. Testing API health..."
curl -s --max-time 10 "$API_URL/health" | jq -r '.status' 2>/dev/null && echo " ✅" || echo " ❌"
echo ""

echo "=== Summary ==="
echo "Web UI: $WEB_UI_URL"
echo "API: $API_URL"
echo ""
echo "To override URLs, use:"
echo "  WEB_UI_URL=http://custom-url:8501 API_URL=http://custom-api:8080 ./test_web_ui_access.sh"
