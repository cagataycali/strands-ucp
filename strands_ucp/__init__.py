"""
Strands UCP - Universal Commerce Protocol tools for Strands Agents

Provides full passthrough access to UCP-compliant merchant APIs for agentic commerce.
"""

from .ucp import (
    ucp,
    ucp_discover,
    ucp_checkout_session,
    ucp_apply_discount,
    ucp_complete_checkout,
)

__version__ = "0.1.0"
__all__ = [
    "ucp",
    "ucp_discover",
    "ucp_checkout_session",
    "ucp_apply_discount",
    "ucp_complete_checkout",
]
