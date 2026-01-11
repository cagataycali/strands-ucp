"""Test script for strands-ucp"""

from strands_ucp import ucp_discover

# Test discovery with local server (if running)
# Start server with: cd ../ucp-samples/rest/python/server && python server.py --port 8182
if __name__ == "__main__":
    result = ucp_discover("http://localhost:8182")
    if result["status"] == "success":
        print("✅ Discovery successful!")
        print(f"UCP Version: {result['body']['ucp']['version']}")
        print(f"Services: {list(result['body']['ucp']['services'].keys())}")
        print(
            f"Capabilities: {len(result['body']['ucp']['capabilities'])} capabilities"
        )
        print(
            f"Payment Handlers: {len(result['body']['payment']['handlers'])} handlers"
        )
    else:
        print(f"❌ Discovery failed: {result.get('message')}")
