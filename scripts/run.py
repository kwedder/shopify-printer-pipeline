#!/usr/bin/env python3
"""
Dilmun Protocol Unified Runner

Single entry point for all protocol operations using the memory middleware.
"""

import sys
import os
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env files
for env_path in [
    "/home/kworqs/.pi/config/.env",
    "/home/kworqs/.env",
    ".env",
]:
    if os.path.exists(env_path):
        load_dotenv(env_path)
        break

# Add skills directory to path for obsidian-dilmun package
SCRIPT_DIR = Path(__file__).parent.parent  # /home/kworqs/.pi/skills/dilmun-protocol
sys.path.insert(0, str(SCRIPT_DIR.parent))  # /home/kworqs/.pi/skills
sys.path.insert(0, str(SCRIPT_DIR.parent / "obsidian_dilmun"))  # /home/kworqs/.pi/skills/obsidian_dilmun

from obsidian_dilmun import DilmunMemoryMiddleware


def action_init(middleware):
    """Initialize protocol services."""
    print("=== Initializing Dilmun Protocol ===")
    state = middleware.init_protocol()
    
    for key, val in state.items():
        status = val.get('status', 'ok')
        print(f"  {key}: {status}")
    
    # Save state to memory-store
    middleware.write_fact("protocol", "status", "initialized", scope="middleware")
    middleware.write_fact("protocol", "version", "2.0.0", scope="middleware")
    
    print("\n=== Ready ===")
    return state


def action_state(middleware):
    """Dump current protocol state."""
    import json
    state = middleware.get_state()
    print(json.dumps(state, indent=2))


def action_workflow(middleware, plate_text=None):
    """Run Goon Plates workflow."""
    print(f"=== Goon Plates Workflow ===")
    
    # Open episode for this workflow
    episode_id = middleware.open_episode("plate_creation", ["shopify", "goon-plates"])
    print(f"Episode: {episode_id}")
    
    # Record the request
    middleware.write_fact("workflow", "plate_request", plate_text or "DEFAULT", scope="goon-plates")
    
    # Publish event for other skills
    middleware.publish("plate.create", {
        "text": plate_text or "GOON",
        "episode": episode_id
    })
    
    # Get scoped context
    context = middleware.get_context()
    print(f"Context facts: {len(context)}")
    
    middleware.close_episode()
    print("=== Workflow Complete ===")


def action_research(middleware, query=None):
    """Run research workflow."""
    print("=== Research Workflow ===")
    
    episode_id = middleware.open_episode("research", ["obsidian-dilmun", "research"])
    
    # Record query
    middleware.write_fact("research", "query", query or "unspecified", scope="research")
    
    # Publish event for external handling
    middleware.publish("research.start", {
        "query": query,
        "episode": episode_id
    })
    
    print(f"Research request recorded: {query or 'unspecified'}")
    print("Use external tools for web search and fact ingestion")
    
    middleware.close_episode()
    print("=== Research Complete ===")


def action_shopify_orders(middleware):
    """Fetch pending Shopify orders."""
    import os
    import json
    import requests
    from datetime import datetime
    import urllib3
    
    # Disable SSL warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    print("=== Shopify Orders ===")
    
    shop_url = os.environ.get("SHOPIFY_SHOP")
    access_token = os.environ.get("SHOPIFY_ACCESS_TOKEN")
    
    # Ensure proper shop URL format
    if shop_url and not shop_url.endswith('.myshopify.com'):
        shop_url = f"{shop_url}.myshopify.com"
    
    if not shop_url or not access_token:
        print("No Shopify credentials configured.")
        print("Set SHOPIFY_SHOP and SHOPIFY_ACCESS_TOKEN environment variables.")
        return
    
    print(f"Shop: {shop_url}")
    print("Fetching pending orders...")
    
    # Open episode
    episode_id = middleware.open_episode("shopify_orders", ["shopify", "orders"])
    
    try:
        # Record the fetch action
        timestamp = datetime.now().isoformat()
        middleware.write_fact("shopify", "last_fetch", timestamp, scope="shopify")
        
        # Fetch orders using requests
        url = f"https://{shop_url}/admin/api/2024-10/orders.json"
        headers = {"X-Shopify-Access-Token": access_token}
        
        response = requests.get(url, headers=headers, verify=False, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        orders = []
        for order_data in data.get("orders", []):
            if order_data.get("financial_status") == "pending":
                orders.append({
                    "id": int(order_data.get("id")),
                    "name": order_data.get("name"),
                    "email": order_data.get("email"),
                    "total_price": float(order_data.get("total_price", 0)),
                    "financial_status": order_data.get("financial_status"),
                })
        
        print(f"Found: {len(orders)} pending orders\n")
        
        middleware.write_fact("shopify", "pending_orders_count", str(len(orders)), scope="orders")
        
        for o in orders[:5]:
            print(f"  {o['name']}: ${o['total_price']} ({o['financial_status']})")
            middleware.write_fact("order", str(o['id']), str(o['name']), scope="orders")
        
        # Publish event
        middleware.publish("shopify.orders.fetched", {
            "count": len(orders),
            "timestamp": timestamp,
            "episode": episode_id
        })
        
        print(f"\n✅ Recorded {len(orders)} orders in protocol state")
        
    except Exception as e:
        print(f"Error fetching orders: {e}")
        middleware.write_fact("shopify", "fetch_error", str(e), scope="orders")
    finally:
        middleware.close_episode()


def action_resolve_conflicts(middleware):
    """Resolve conflicts using ring theory principles."""
    from pathlib import Path
    import importlib.util
    
    # Import the resolver
    resolver_path = Path(__file__).parent / "resolve_conflicts.py"
    spec = importlib.util.spec_from_file_location("resolve_conflicts", resolver_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load resolver from {resolver_path}")
    resolver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(resolver)
    
    return resolver.resolve_all()


def action_enhanced_search(middleware, query=None, k=10):
    """Search facts using vector similarity."""
    import importlib.util
    
    # Import enhanced memory
    enh_path = Path(__file__).parent / "enhanced_memory.py"
    spec = importlib.util.spec_from_file_location("enhanced_memory", enh_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load enhanced_memory from {enh_path}")
    enh = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(enh)
    
    return enh.vector_search(query or "unspecified", k=k)


def action_write_embedded(middleware, entity=None, predicate=None, value=None, scope=None):
    """Write a fact with embedding for similarity search."""
    import importlib.util
    
    # Import enhanced memory
    enh_path = Path(__file__).parent / "enhanced_memory.py"
    spec = importlib.util.spec_from_file_location("enhanced_memory", enh_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load enhanced_memory from {enh_path}")
    enh = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(enh)
    
    return enh.write_fact_with_embedding(entity, predicate, value, scope)


def main():
    parser = argparse.ArgumentParser(description="Dilmun Protocol Runner")
    parser.add_argument("--action", choices=["init", "state", "workflow", "research", "shopify-orders", "resolve-conflicts", "enhanced-search", "write-embedded"],
                       required=True, help="Action to perform")
    parser.add_argument("--plate-text", help="Text for plate creation")
    parser.add_argument("--query", help="Research query or search query")
    parser.add_argument("--entity", help="Entity for embedded fact")
    parser.add_argument("--predicate", help="Predicate for embedded fact")
    parser.add_argument("--value", help="Value for embedded fact")
    parser.add_argument("--scope", help="Scope for embedded fact")
    parser.add_argument("--k", type=int, default=10, help="Number of results for search")
    
    args = parser.parse_args()
    
    middleware = DilmunMemoryMiddleware()
    
    if args.action == "init":
        action_init(middleware)
    elif args.action == "state":
        action_state(middleware)
    elif args.action == "workflow":
        action_workflow(middleware, args.plate_text)
    elif args.action == "research":
        action_research(middleware, args.query)
    elif args.action == "shopify-orders":
        action_shopify_orders(middleware)
    elif args.action == "resolve-conflicts":
        action_resolve_conflicts(middleware)
    elif args.action == "enhanced-search":
        results = action_enhanced_search(middleware, args.query, args.k)
        import json
        print(json.dumps(results, indent=2))
    elif args.action == "write-embedded":
        action_write_embedded(middleware, args.entity, args.predicate, args.value, args.scope)


if __name__ == "__main__":
    main()