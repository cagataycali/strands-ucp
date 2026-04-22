# Strands UCP

[![Awesome Strands Agents](https://img.shields.io/badge/Awesome-Strands%20Agents-00FF77?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjkwIiBoZWlnaHQ9IjQ2MyIgdmlld0JveD0iMCAwIDI5MCA0NjMiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik05Ny4yOTAyIDUyLjc4ODRDODUuMDY3NCA0OS4xNjY3IDcyLjIyMzQgNTYuMTM4OSA2OC42MDE3IDY4LjM2MTZDNjQuOTgwMSA4MC41ODQzIDcxLjk1MjQgOTMuNDI4MyA4NC4xNzQ5IDk3LjA1MDFMMjM1LjExNyAxMzkuNzc1QzI0NS4yMjMgMTQyLjc2OSAyNDYuMzU3IDE1Ni42MjggMjM2Ljg3NCAxNjEuMjI2TDMyLjU0NiAyNjAuMjkxQy0xNC45NDM5IDI4My4zMTYgLTkuMTYxMDcgMzUyLjc0IDQxLjQ4MzUgMzY3LjU5MUwxODkuNTUxIDQxMS4wMDlMMTkwLjEyNSA0MTEuMTY5QzIwMi4xODMgNDE0LjM3NiAyMTQuNjY1IDQwNy4zOTYgMjE4LjE5NiAzOTUuMzU1QzIyMS43ODQgMzgzLjEyMiAyMTQuNzc0IDM3MC4yOTYgMjAyLjU0MSAzNjYuNzA5TDU0LjQ3MzggMzIzLjI5MUM0NC4zNDQ3IDMyMC4zMjEgNDMuMTg3OSAzMDYuNDM2IDUyLjY4NTcgMzAxLjgzMUwyNTcuMDE0IDIwMi43NjZDMzA0LjQzMiAxNzkuNzc2IDI5OC43NTggMTEwLjQ4MyAyNDguMjMzIDk1LjUxMkw5Ny4yOTAyIDUyLjc4ODRaIiBmaWxsPSIjRkZGRkZGIi8+CjxwYXRoIGQ9Ik0yNTkuMTQ3IDAuOTgxODEyQzI3MS4zODkgLTIuNTc0OTggMjg0LjE5NyA0LjQ2NTcxIDI4Ny43NTQgMTYuNzA3NEMyOTEuMzExIDI4Ljk0OTIgMjg0LjI3IDQxLjc1NyAyNzIuMDI4IDQ1LjMxMzhMNzEuMTcyNyAxMDMuNjcxQzQwLjcxNDIgMTEyLjUyMSAzNy4xOTc2IDE1NC4yNjIgNjUuNzQ1OSAxNjguMDgzTDI0MS4zNDMgMjUzLjA5M0MzMDcuODcyIDI4NS4zMDIgMjk5Ljc5NCAzODIuNTQ2IDIyOC44NjIgNDAzLjMzNkwzMC40MDQxIDQ2MS41MDJDMTguMTcwNyA0NjUuMDg4IDUuMzQ3MDggNDU4LjA3OCAxLjc2MTUzIDQ0NS44NDRDLTEuODIzOSA0MzMuNjExIDUuMTg2MzcgNDIwLjc4NyAxNy40MTk3IDQxNy4yMDJMMjE1Ljg3OCAzNTkuMDM1QzI0Ni4yNzcgMzUwLjEyNSAyNDkuNzM5IDMwOC40NDkgMjIxLjIyNiAyOTQuNjQ1TDQ1LjYyOTcgMjA5LjYzNUMtMjAuOTgzNCAxNzcuMzg2IC0xMi43NzcyIDc5Ljk4OTMgNTguMjkyOCA1OS4zNDAyTDI1OS4xNDcgMC45ODE4MTJaIiBmaWxsPSIjRkZGRkZGIi8+Cjwvc3ZnPgo=&logoColor=white)](https://github.com/cagataycali/awesome-strands-agents)

**Universal Commerce Protocol (UCP) tools for Strands Agents**

Enable agentic commerce experiences with full UCP protocol support: discovery, checkout, orders, payments, and extensions.

[![PyPI version](https://badge.fury.io/py/strands-ucp.svg)](https://badge.fury.io/py/strands-ucp)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## 🚀 Features

- **🔍 Discovery** - Query merchant capabilities, services, and payment handlers
- **🛒 Checkout** - Full lifecycle management (create → update → complete)
- **📦 Orders** - Get, list, cancel, and update orders
- **💰 Payments** - Multi-handler support with automatic header management
- **🔐 Security** - Request signature support (parameter + env var)
- **🎟️ Extensions** - Discounts, fulfillment, refunds, returns, disputes
- **🔧 Custom** - Passthrough for any UCP endpoint

## 📦 Installation

```bash
pip install strands-ucp
```

## 🎯 Quick Start

```python
from strands_ucp import ucp_discover, ucp_checkout_session, ucp_apply_discount, ucp_complete_checkout

# 1. Discover merchant capabilities
discovery = ucp_discover("https://shop.example.com")
handlers = discovery["body"]["payment"]["handlers"]

# 2. Create checkout session (with optional signature)
checkout = ucp_checkout_session(
    merchant_url="https://shop.example.com",
    line_items=[
        {"item": {"id": "product_123", "title": "Widget"}, "quantity": 2}
    ],
    currency="USD",
    payment_handlers=handlers,
    buyer={"full_name": "John Doe", "email": "john@example.com"},
    request_signature="eyJhbGc..."  # Optional: JWT/signed token
)

# 3. Apply discount code
checkout = ucp_apply_discount(
    merchant_url="https://shop.example.com",
    checkout_id=checkout["checkout_id"],
    discount_codes=["SAVE10"],
    current_checkout=checkout["body"]
)

# 4. Complete checkout
order = ucp_complete_checkout(
    merchant_url="https://shop.example.com",
    checkout_id=checkout["checkout_id"],
    payment_instrument={
        "type": "card",
        "handler_id": "mock_payment_handler",
        "credential": {"token": "success_token"}
    }
)

print(f"Order created: {order['order_id']}")
```

## 🔐 Security & Signatures

### Request Signatures

Production UCP merchants require request signatures for security. Provide them via:

**1. Function Parameter (Recommended)**
```python
ucp_checkout_session(
    merchant_url="https://shop.example.com",
    request_signature="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    # ... other params
)
```

**2. Environment Variable**
```bash
export UCP_REQUEST_SIGNATURE="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

```python
# Signature automatically loaded from env var
ucp_checkout_session(
    merchant_url="https://shop.example.com",
    # ... other params
)
```

**Parameter takes precedence over env var.** If neither is provided, the `request-signature` header is omitted (discovery endpoints typically don't require signatures).

### Generating Signatures

Request signatures are typically JWT tokens signed with your merchant credentials:

```python
import jwt
import time

def generate_request_signature(merchant_secret: str, request_data: dict) -> str:
    payload = {
        "iat": int(time.time()),
        "exp": int(time.time()) + 300,  # 5 min expiry
        "data": request_data
    }
    return jwt.encode(payload, merchant_secret, algorithm="HS256")

# Use in request
signature = generate_request_signature("your-secret-key", {"merchant_id": "123"})
ucp_checkout_session(..., request_signature=signature)
```

## 📚 Available Functions

### Core Function

#### `ucp(action, merchant_url, **kwargs)`

Generic UCP client supporting all operations.

**Actions:**
- `discovery` - Get merchant capabilities
- `checkout_create` - Create checkout session
- `checkout_get` - Get checkout session
- `checkout_update` - Update checkout
- `checkout_complete` - Complete checkout with payment
- `order_get` - Get order details
- `order_list` - List orders
- `order_cancel` - Cancel order
- `order_update` - Update order
- `refund_create` - Create refund
- `return_create` - Create return
- `dispute_create` - Create dispute
- `custom` - Custom endpoint access

**Parameters:**
- `action` (str) - UCP action to perform
- `merchant_url` (str) - Merchant base URL
- `method` (str) - HTTP method (auto-set for standard actions)
- `endpoint` (str) - Custom endpoint path
- `headers` (dict) - Additional headers
- `body` (dict) - Request body
- `checkout_id` (str) - Checkout session ID
- `order_id` (str) - Order ID
- `request_signature` (str) - Request signature (JWT/token)
- `auto_headers` (bool) - Auto-add UCP headers (default: True)
- `timeout` (int) - Request timeout in seconds
- `follow_redirects` (bool) - Follow redirects (default: True)

### Helper Functions

#### `ucp_discover(merchant_url)`
Discover merchant capabilities and services.

#### `ucp_checkout_session(merchant_url, line_items, currency, payment_handlers, buyer=None, request_signature=None)`
Create a new checkout session with optional buyer info and signature.

#### `ucp_apply_discount(merchant_url, checkout_id, discount_codes, current_checkout, request_signature=None)`
Apply discount codes to checkout with optional signature.

#### `ucp_complete_checkout(merchant_url, checkout_id, payment_instrument, risk_signals=None, request_signature=None)`
Complete checkout with payment and optional signature.

## 🔧 Advanced Usage

### Custom Requests

```python
from strands_ucp import ucp

# Custom endpoint with signature
result = ucp(
    action="custom",
    merchant_url="https://shop.example.com",
    method="POST",
    endpoint="/api/custom-action",
    body={"custom_field": "value"},
    request_signature="eyJhbGc..."
)
```

### Manual Header Control

```python
from strands_ucp import ucp

result = ucp(
    action="checkout_create",
    merchant_url="https://shop.example.com",
    body={...},
    auto_headers=False,  # Disable automatic headers
    headers={
        "UCP-Agent": 'profile="https://my-agent/profile"',
        "request-id": "custom-request-id",
        "request-signature": "signed-jwt-token",
        "idempotency-key": "custom-idempotency-key"
    }
)
```

### Order Management

```python
from strands_ucp import ucp

# Get order
order = ucp(
    action="order_get",
    merchant_url="https://shop.example.com",
    order_id="order_abc123"
)

# Cancel order
ucp(
    action="order_cancel",
    merchant_url="https://shop.example.com",
    order_id="order_abc123",
    body={"reason": "Customer request"},
    request_signature="eyJhbGc..."
)

# Create refund
ucp(
    action="refund_create",
    merchant_url="https://shop.example.com",
    order_id="order_abc123",
    body={"amount": 2500, "reason": "Defective product"},
    request_signature="eyJhbGc..."
)
```

### Environment-Based Configuration

```bash
# Set signature once for all requests
export UCP_REQUEST_SIGNATURE="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Optional: Set custom agent profile
export UCP_AGENT_PROFILE="https://my-company.com/agent-profile"
```

```python
# Signature automatically loaded from env
from strands_ucp import ucp_checkout_session

checkout = ucp_checkout_session(
    merchant_url="https://shop.example.com",
    line_items=[...],
    currency="USD",
    payment_handlers=[...]
    # request_signature loaded from UCP_REQUEST_SIGNATURE env var
)
```

## 📖 Response Format

All functions return a dictionary with:

```python
{
    "status": "success" | "error",
    "status_code": 200,
    "headers": {...},
    "body": {...},  # Parsed JSON response
    "ucp_metadata": {...},  # UCP metadata (when available)
    "capabilities": [...],   # Capabilities (when available)
    "checkout_id": "...",    # Checkout ID (when available)
    "order_id": "...",       # Order ID (when available)
    "request": {
        "method": "POST",
        "url": "...",
        "headers": {...},  # Note: request-signature excluded from logs
        "body": {...}
    }
}
```

**Security Note:** The `request-signature` header is excluded from response logs for security.

## 🧪 Testing

Test with the official UCP sample server:

```bash
# Clone samples
git clone https://github.com/Universal-Commerce-Protocol/samples.git
cd samples/rest/python/server

# Install and run
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python server.py --port 8182
```

Then test:

```python
from strands_ucp import ucp_discover

result = ucp_discover("http://localhost:8182")
print(result)
```

### Testing with Signatures

The sample server may accept test signatures:

```python
from strands_ucp import ucp_checkout_session

checkout = ucp_checkout_session(
    merchant_url="http://localhost:8182",
    line_items=[{"item": {"id": "test_item"}, "quantity": 1}],
    currency="USD",
    payment_handlers=[...],
    request_signature="test"  # Test servers may accept this
)
```

**Production:** Always use properly signed JWT tokens in production.

## 🔗 Protocol Details

### Required Headers

Automatically added by the tool (when `auto_headers=True`):
- `UCP-Agent` - Agent profile identifier
- `request-id` - Unique request ID (UUID)
- `idempotency-key` - For safe retries (POST/PUT/PATCH)
- `request-signature` - Request signature (if provided via parameter or env var)

### Discovery Endpoint

`GET /.well-known/ucp` returns:
- UCP version
- Supported services
- Capabilities (checkout, order, discounts, etc.)
- Payment handlers
- Transport bindings (REST, MCP, A2A)

### Standard Endpoints

- **Checkout**: `/checkout-sessions`, `/checkout-sessions/{id}`, `/checkout-sessions/{id}/complete`
- **Orders**: `/orders`, `/orders/{id}`, `/orders/{id}/cancel`
- **Extensions**: `/orders/{id}/refunds`, `/orders/{id}/returns`, `/orders/{id}/disputes`

## 🌐 Resources

- **UCP Specification**: https://ucp.dev
- **Python SDK**: https://github.com/Universal-Commerce-Protocol/python-sdk
- **Samples**: https://github.com/Universal-Commerce-Protocol/samples
- **Google Integration**: https://developers.google.com/merchant/ucp
- **Blog Post**: https://developers.googleblog.com/under-the-hood-universal-commerce-protocol-ucp/

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

Apache License 2.0 - See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built on [Strands Agents](https://github.com/strands-ai/strands-agents)
- Implements [Universal Commerce Protocol (UCP)](https://ucp.dev)
