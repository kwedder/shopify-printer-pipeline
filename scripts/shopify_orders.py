#!/usr/bin/env python3
"""
Dilmun Protocol Shopify Integration

Fetches pending orders from Shopify and records them in the protocol state.
"""

import sys
import os
import json
from pathlib import Path

# Add skills directory to path
SKILLS_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILLS_DIR))

from obsidian_dilmun import DilmunMemoryMiddleware
import shopify


def setup_shopify():
    """Set up Shopify API session."""
    shop_url = os.environ.get("SHOPIFY_SHOP")
    access_token = os.environ.get("SHOPIFY_ACCESS_TOKEN")
    
    if not shop_url or not access_token:
        return None
    
    session = shopify.Session(shop_url, "2023-10", access_token)
    shopify.ShopifyResource.activate_session(session)
    return access_token


def fetch_pending_orders():
    """Fetch pending orders from Shopify."""
    orders = []
    for order in shopify.Order.find(status="any", limit=250):
        if order.financial_status == "pending":
            orders.append({
                "id": int(order.id),
                "name": order.name,
                "email": order.email,
                "total_price": float(order.total_price),
                "financial_status": order.financial_status,
                "fulfillment_status": order.fulfillment_status or "unfulfilled",
                "created_at": order.created_at,
            })
    return orders


def main():
    # Initialize middleware
    middleware = DilmunMemoryMiddleware()
    
    # Set up Shopify
    access_token = setup_shopify()
    
    if not access_token:
        print("=== Shopify Orders ===")
        print("No Shopify credentials configured.")
        print("Set SHOPIFY_SHOP and SHOPIFY_ACCESS_TOKEN environment variables.")
        return
    
    # Open episode
    episode_id = middleware.open_episode("shopify_orders", ["shopify", "orders"])
    
    try:
        # Fetch orders
        orders = fetch_pending_orders()
        
        print("=== Shopify Pending Orders ===")
        print(f"Found: {len(orders)} pending orders\n")
        
        # Record in memory-store
        middleware.write_fact("shopify", "pending_orders_count", str(len(orders)), scope="orders")
        
        for order in orders[:5]:  # Show first 5
            print(f"  {order['name']}: ${order['total_price']} ({order['financial_status']})")
            print(f"    Email: {order['email']}")
            middleware.write_fact("order", str(order['id']), json.dumps(order), scope="orders")
        
        # Publish event
        middleware.publish("shopify.orders.fetched", {
            "count": len(orders),
            "episode": episode_id
        })
        
        print(f"\n✅ Recorded {len(orders)} orders in protocol state")
        
    finally:
        middleware.close_episode()


if __name__ == "__main__":
    main()