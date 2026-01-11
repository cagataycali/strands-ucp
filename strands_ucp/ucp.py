#!/usr/bin/env python3
"""
Universal Commerce Protocol (UCP) Tool for Strands

A generic passthrough tool for interacting with UCP-compliant merchants.
Supports discovery, checkout, orders, and all UCP capabilities.

Licensed under the Apache License, Version 2.0
"""

import os
import uuid
import json
from typing import Dict, Any, Optional, List
import httpx
from strands import tool


@tool
def ucp(
    action: str,
    merchant_url: str,
    method: str = "GET",
    endpoint: str = "",
    headers: Optional[Dict[str, str]] = None,
    body: Optional[Dict[str, Any]] = None,
    checkout_id: Optional[str] = None,
    order_id: Optional[str] = None,
    request_signature: Optional[str] = None,
    auto_headers: bool = True,
    timeout: int = 30,
    follow_redirects: bool = True,
) -> Dict[str, Any]:
    """
    Universal Commerce Protocol (UCP) client tool.

    Provides full passthrough access to UCP-compliant merchant APIs with automatic
    header management, request/response validation, and support for all UCP capabilities.

    Args:
        action: UCP action to perform:
            - "discovery" - Discover merchant capabilities (GET /.well-known/ucp)
            - "checkout_create" - Create new checkout session (POST /checkout-sessions)
            - "checkout_get" - Get checkout session (GET /checkout-sessions/{id})
            - "checkout_update" - Update checkout (PUT /checkout-sessions/{id})
            - "checkout_complete" - Complete checkout (POST /checkout-sessions/{id}/complete)
            - "order_get" - Get order details (GET /orders/{id})
            - "order_list" - List orders (GET /orders)
            - "order_cancel" - Cancel order (POST /orders/{id}/cancel)
            - "order_update" - Update order (PUT /orders/{id})
            - "refund_create" - Create refund (POST /orders/{id}/refunds)
            - "return_create" - Create return (POST /orders/{id}/returns)
            - "dispute_create" - Create dispute (POST /orders/{id}/disputes)
            - "custom" - Custom request with manual endpoint/method
        merchant_url: Base URL of the UCP merchant (e.g., "https://shop.example.com")
        method: HTTP method (GET, POST, PUT, PATCH, DELETE) - auto-set for standard actions
        endpoint: Custom endpoint path (for "custom" action)
        headers: Additional HTTP headers (UCP headers added automatically if auto_headers=True)
        body: Request body as dict (will be JSON-encoded)
        checkout_id: Checkout session ID (for checkout operations)
        order_id: Order ID (for order operations)
        request_signature: Request signature (JWT/signed token). Falls back to UCP_REQUEST_SIGNATURE env var.
        auto_headers: Automatically add UCP-required headers (default: True)
        timeout: Request timeout in seconds
        follow_redirects: Follow HTTP redirects

    Returns:
        Dict with:
            - status: "success" or "error"
            - status_code: HTTP status code
            - headers: Response headers
            - body: Parsed response body
            - ucp_metadata: Extracted UCP metadata if present
            - capabilities: List of capabilities if discovery response
            - checkout_id: Checkout ID if checkout response
            - order_id: Order ID if order response

    Examples:
        # Discover merchant capabilities
        ucp(action="discovery", merchant_url="https://shop.example.com")

        # Create checkout session with signature
        ucp(
            action="checkout_create",
            merchant_url="https://shop.example.com",
            request_signature="eyJhbGc...",
            body={
                "line_items": [{"item": {"id": "product_123"}, "quantity": 1}],
                "currency": "USD",
                "payment": {"instruments": [], "handlers": [...]}
            }
        )

        # Update checkout with discount
        ucp(
            action="checkout_update",
            merchant_url="https://shop.example.com",
            checkout_id="checkout_abc123",
            body={
                "id": "checkout_abc123",
                "line_items": [...],
                "discounts": {"codes": ["SAVE10"]}
            }
        )

        # Complete checkout
        ucp(
            action="checkout_complete",
            merchant_url="https://shop.example.com",
            checkout_id="checkout_abc123",
            body={
                "payment_data": {
                    "type": "card",
                    "credential": {"token": "payment_token_xyz"}
                }
            }
        )

        # Get order details
        ucp(action="order_get", merchant_url="https://shop.example.com", order_id="order_xyz")

        # Custom request
        ucp(
            action="custom",
            merchant_url="https://shop.example.com",
            method="POST",
            endpoint="/custom-endpoint",
            body={"custom": "data"}
        )
    """

    try:
        # Action-to-endpoint mapping
        action_map = {
            "discovery": {
                "method": "GET",
                "endpoint": "/.well-known/ucp",
            },
            "checkout_create": {
                "method": "POST",
                "endpoint": "/checkout-sessions",
            },
            "checkout_get": {
                "method": "GET",
                "endpoint": (
                    f"/checkout-sessions/{checkout_id}"
                    if checkout_id
                    else "/checkout-sessions"
                ),
            },
            "checkout_update": {
                "method": "PUT",
                "endpoint": (
                    f"/checkout-sessions/{checkout_id}"
                    if checkout_id
                    else "/checkout-sessions"
                ),
            },
            "checkout_complete": {
                "method": "POST",
                "endpoint": (
                    f"/checkout-sessions/{checkout_id}/complete"
                    if checkout_id
                    else "/checkout-sessions/complete"
                ),
            },
            "order_get": {
                "method": "GET",
                "endpoint": f"/orders/{order_id}" if order_id else "/orders",
            },
            "order_list": {
                "method": "GET",
                "endpoint": "/orders",
            },
            "order_cancel": {
                "method": "POST",
                "endpoint": (
                    f"/orders/{order_id}/cancel" if order_id else "/orders/cancel"
                ),
            },
            "order_update": {
                "method": "PUT",
                "endpoint": f"/orders/{order_id}" if order_id else "/orders",
            },
            "refund_create": {
                "method": "POST",
                "endpoint": (
                    f"/orders/{order_id}/refunds" if order_id else "/orders/refunds"
                ),
            },
            "return_create": {
                "method": "POST",
                "endpoint": (
                    f"/orders/{order_id}/returns" if order_id else "/orders/returns"
                ),
            },
            "dispute_create": {
                "method": "POST",
                "endpoint": (
                    f"/orders/{order_id}/disputes" if order_id else "/orders/disputes"
                ),
            },
        }

        # Determine method and endpoint
        if action == "custom":
            final_method = method
            final_endpoint = endpoint
        elif action in action_map:
            final_method = action_map[action]["method"]
            final_endpoint = action_map[action]["endpoint"]
        else:
            return {
                "status": "error",
                "message": f"Unknown action: {action}. Use 'custom' for manual requests.",
                "valid_actions": list(action_map.keys()) + ["custom"],
            }

        # Build full URL
        url = f"{merchant_url.rstrip('/')}{final_endpoint}"

        # Prepare headers
        request_headers = headers or {}

        # Add UCP-required headers automatically
        if auto_headers:
            if "UCP-Agent" not in request_headers:
                request_headers["UCP-Agent"] = 'profile="https://strands.dev/profile"'
            if "request-id" not in request_headers:
                request_headers["request-id"] = str(uuid.uuid4())
            if "idempotency-key" not in request_headers and final_method in [
                "POST",
                "PUT",
                "PATCH",
            ]:
                request_headers["idempotency-key"] = str(uuid.uuid4())

            # Add request signature if provided (parameter or env var)
            if "request-signature" not in request_headers:
                signature = request_signature or os.getenv("UCP_REQUEST_SIGNATURE")
                if signature:
                    request_headers["request-signature"] = signature
                # Note: If no signature provided, header is omitted (required for production UCP)

        # Add Content-Type for requests with body
        if body and "Content-Type" not in request_headers:
            request_headers["Content-Type"] = "application/json"

        # Make the request
        with httpx.Client(timeout=timeout, follow_redirects=follow_redirects) as client:
            if final_method == "GET":
                response = client.get(url, headers=request_headers)
            elif final_method == "POST":
                response = client.post(url, json=body, headers=request_headers)
            elif final_method == "PUT":
                response = client.put(url, json=body, headers=request_headers)
            elif final_method == "PATCH":
                response = client.patch(url, json=body, headers=request_headers)
            elif final_method == "DELETE":
                response = client.delete(url, headers=request_headers)
            else:
                return {
                    "status": "error",
                    "message": f"Unsupported HTTP method: {final_method}",
                }

        # Parse response
        try:
            response_body = response.json()
        except json.JSONDecodeError:
            response_body = response.text

        # Extract UCP metadata
        ucp_metadata = None
        capabilities = []
        response_checkout_id = None
        response_order_id = None

        if isinstance(response_body, dict):
            # Extract UCP metadata from response
            if "ucp" in response_body:
                ucp_metadata = response_body["ucp"]
                if "capabilities" in ucp_metadata:
                    capabilities = ucp_metadata["capabilities"]

            # Extract IDs
            if "id" in response_body:
                if action.startswith("checkout"):
                    response_checkout_id = response_body["id"]
                elif action.startswith("order"):
                    response_order_id = response_body["id"]

            # For order in checkout response
            if "order" in response_body and isinstance(response_body["order"], dict):
                if "id" in response_body["order"]:
                    response_order_id = response_body["order"]["id"]

        # Build result
        result = {
            "status": "success" if response.is_success else "error",
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response_body,
            "request": {
                "method": final_method,
                "url": url,
                "headers": {
                    k: v for k, v in request_headers.items() if k != "request-signature"
                },  # Don't log signature
                "body": body,
            },
        }

        # Add extracted metadata
        if ucp_metadata:
            result["ucp_metadata"] = ucp_metadata
        if capabilities:
            result["capabilities"] = capabilities
        if response_checkout_id:
            result["checkout_id"] = response_checkout_id
        if response_order_id:
            result["order_id"] = response_order_id

        return result

    except httpx.TimeoutException as e:
        return {
            "status": "error",
            "message": f"Request timeout: {str(e)}",
            "timeout": timeout,
        }
    except httpx.RequestError as e:
        return {
            "status": "error",
            "message": f"Request error: {str(e)}",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}",
        }


# Helper functions for common UCP operations


@tool
def ucp_discover(merchant_url: str) -> Dict[str, Any]:
    """
    Discover UCP merchant capabilities.

    Queries the merchant's /.well-known/ucp endpoint to retrieve:
    - Supported UCP version
    - Available services (shopping, etc.)
    - Capabilities (checkout, order, discounts, fulfillment, etc.)
    - Payment handlers
    - Transport bindings (REST, MCP, A2A)

    Args:
        merchant_url: Base URL of the UCP merchant

    Returns:
        Dict with discovery data including services, capabilities, and payment handlers

    Example:
        ucp_discover(merchant_url="https://shop.example.com")
    """
    return ucp(action="discovery", merchant_url=merchant_url)


@tool
def ucp_checkout_session(
    merchant_url: str,
    line_items: List[Dict[str, Any]],
    currency: str,
    payment_handlers: List[Dict[str, Any]],
    buyer: Optional[Dict[str, Any]] = None,
    request_signature: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a new UCP checkout session.

    Args:
        merchant_url: Base URL of the UCP merchant
        line_items: List of items with format [{"item": {"id": "...", "title": "..."}, "quantity": N}]
        currency: ISO 4217 currency code (e.g., "USD")
        payment_handlers: List of payment handlers from discovery
        buyer: Optional buyer information {"full_name": "...", "email": "..."}
        request_signature: Optional request signature (JWT/signed token)

    Returns:
        Dict with checkout session details including checkout_id

    Example:
        ucp_checkout_session(
            merchant_url="https://shop.example.com",
            line_items=[{"item": {"id": "product_123"}, "quantity": 1}],
            currency="USD",
            payment_handlers=[...],  # From discovery
            buyer={"full_name": "John Doe", "email": "john@example.com"},
            request_signature="eyJhbGc..."
        )
    """
    body = {
        "line_items": line_items,
        "currency": currency,
        "payment": {
            "instruments": [],
            "handlers": payment_handlers,
        },
    }

    if buyer:
        body["buyer"] = buyer

    return ucp(
        action="checkout_create",
        merchant_url=merchant_url,
        body=body,
        request_signature=request_signature,
    )


@tool
def ucp_apply_discount(
    merchant_url: str,
    checkout_id: str,
    discount_codes: List[str],
    current_checkout: Dict[str, Any],
    request_signature: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Apply discount codes to a checkout session.

    Args:
        merchant_url: Base URL of the UCP merchant
        checkout_id: Checkout session ID
        discount_codes: List of discount codes to apply (e.g., ["SAVE10"])
        current_checkout: Current checkout session data (from previous response)
        request_signature: Optional request signature (JWT/signed token)

    Returns:
        Dict with updated checkout including applied discounts

    Example:
        ucp_apply_discount(
            merchant_url="https://shop.example.com",
            checkout_id="checkout_123",
            discount_codes=["SAVE10"],
            current_checkout=checkout_data,
            request_signature="eyJhbGc..."
        )
    """
    # Build update payload with discount
    body = {
        "id": checkout_id,
        "line_items": current_checkout.get("line_items", []),
        "currency": current_checkout.get("currency", "USD"),
        "payment": current_checkout.get("payment", {}),
        "discounts": {
            "codes": discount_codes,
        },
    }

    return ucp(
        action="checkout_update",
        merchant_url=merchant_url,
        checkout_id=checkout_id,
        body=body,
        request_signature=request_signature,
    )


@tool
def ucp_complete_checkout(
    merchant_url: str,
    checkout_id: str,
    payment_instrument: Dict[str, Any],
    risk_signals: Optional[Dict[str, Any]] = None,
    request_signature: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Complete a checkout session with payment.

    Args:
        merchant_url: Base URL of the UCP merchant
        checkout_id: Checkout session ID
        payment_instrument: Payment instrument data matching handler schema
        risk_signals: Optional risk signals (IP, browser, etc.)
        request_signature: Optional request signature (JWT/signed token)

    Returns:
        Dict with completed order details including order_id

    Example:
        ucp_complete_checkout(
            merchant_url="https://shop.example.com",
            checkout_id="checkout_123",
            payment_instrument={
                "type": "card",
                "credential": {"token": "payment_token_xyz"},
                "handler_id": "mock_payment_handler"
            },
            request_signature="eyJhbGc..."
        )
    """
    body = {
        "payment_data": payment_instrument,
    }

    if risk_signals:
        body["risk_signals"] = risk_signals

    return ucp(
        action="checkout_complete",
        merchant_url=merchant_url,
        checkout_id=checkout_id,
        body=body,
        request_signature=request_signature,
    )


if __name__ == "__main__":
    # Test discovery
    print("Testing UCP tool...")
    result = ucp_discover(merchant_url="http://localhost:8182")
    print(json.dumps(result, indent=2))
