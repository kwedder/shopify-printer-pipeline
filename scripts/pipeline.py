#!/usr/bin/env python3
"""
Kworqs Shopify Printer Pipeline

Main entry point for the formal GSD-compliant pipeline that transforms
Shopify orders into 3D printable models via Blender-MCP.

Usage:
    python pipeline.py --action init
    python pipeline.py --action fetch-orders
    python pipeline.py --action process-order ORDER_ID
    python pipeline.py --action workflow --text "YOURTEXT"
"""

import sys
import os
import argparse
import json
from pathlib import Path
from datetime import datetime

# Setup paths for existing skills
SKILLS_ROOT = Path("/home/kworqs/.pi/skills")
sys.path.insert(0, str(SKILLS_ROOT))
sys.path.insert(0, str(SKILLS_ROOT / "obsidian_dilmun"))

from obsidian_dilmun import DilmunMemoryMiddleware


class ShopifyPrinterPipeline:
    """Main pipeline orchestrator."""
    
    def __init__(self):
        self.middleware = DilmunMemoryMiddleware()
        self.vault_path = Path(os.environ.get("DILMUN_VAULT", "/home/kworqs/.pi/subdilmun"))
    
    def init(self):
        """Initialize the pipeline."""
        print("=== Initializing Shopify Printer Pipeline ===")
        
        # Initialize Dilmun protocol
        state = self.middleware.init_protocol()
        for key, val in state.items():
            print(f"  {key}: {val.get('status', 'ok')}")
        
        # Write startup fact
        self.middleware.write_fact(
            "pipeline", "status", "initialized",
            scope="shopify-printer-pipeline"
        )
        
        # Record version
        self.middleware.write_fact(
            "pipeline", "version", "1.0.0",
            scope="shopify-printer-pipeline"
        )
        
        print("\n=== Pipeline Ready ===")
        return {"status": "ok", "timestamp": datetime.now().isoformat()}
    
    def fetch_orders(self):
        """Fetch pending Shopify orders."""
        from shopify_orders import ShopifyClient
        
        print("=== Fetching Shopify Orders ===")
        
        client = ShopifyClient()
        orders = client.get_pending_orders(limit=50)
        
        print(f"Found {len(orders)} pending orders")
        
        # Record orders in Dilmun
        for order in orders:
            self.middleware.write_fact(
                "order", str(order.id), str(order.name),
                scope="shopify"
            )
            self.middleware.publish("order.received", {
                "order_id": order.id,
                "text": order.name,
                "status": "pending"
            })
        
        return {"count": len(orders), "orders": [o.to_dict() for o in orders]}
    
    def process_order(self, order_id, text):
        """Process a single order through the pipeline."""
        print(f"=== Processing Order {order_id} ===")
        
        # Open episode for this workflow
        episode_id = self.middleware.open_episode(
            f"order_{order_id}",
            ["shopify", "goon-plates", "blender-mcp"]
        )
        
        # Record order
        self.middleware.write_fact("plate", str(order_id), "processing", scope="plates")
        
        # Publish event for goon-plates/blender-mcp
        self.middleware.publish("plate.create", {
            "order_id": order_id,
            "text": text,
            "episode": episode_id
        })
        
        print(f"Order {order_id} queued for plate creation")
        print(f"Episode: {episode_id}")
        
        self.middleware.close_episode()
        
        return {
            "order_id": order_id,
            "text": text,
            "status": "queued",
            "episode": episode_id
        }
    
    def workflow(self, text):
        """Run the plate creation workflow."""
        print(f"=== Running Workflow: {text} ===")
        
        episode_id = self.middleware.open_episode(
            "plate_workflow",
            ["shopify", "goon-plates"]
        )
        
        self.middleware.write_fact(
            "workflow", "plate_request", text,
            scope="goon-plates"
        )
        
        self.middleware.publish("plate.create", {
            "text": text,
            "episode": episode_id
        })
        
        self.middleware.close_episode()
        
        return {"status": "ok", "text": text, "episode": episode_id}
    
    def state(self):
        """Get current pipeline state."""
        return self.middleware.get_state()


def main():
    parser = argparse.ArgumentParser(description="Shopify Printer Pipeline")
    parser.add_argument("--action", required=True,
                       choices=["init", "fetch-orders", "process-order", "workflow", "state"],
                       help="Action to perform")
    parser.add_argument("--order-id", type=int, help="Order ID to process")
    parser.add_argument("--text", help="Text for plate creation")
    
    args = parser.parse_args()
    
    pipeline = ShopifyPrinterPipeline()
    result = None
    
    if args.action == "init":
        result = pipeline.init()
    elif args.action == "fetch-orders":
        result = pipeline.fetch_orders()
    elif args.action == "process-order":
        if not args.order_id or not args.text:
            print("Error: --order-id and --text required for process-order")
            sys.exit(1)
        result = pipeline.process_order(args.order_id, args.text)
    elif args.action == "workflow":
        if not args.text:
            print("Error: --text required for workflow")
            sys.exit(1)
        result = pipeline.workflow(args.text)
    elif args.action == "state":
        result = pipeline.state()
    else:
        print("Unknown action")
        sys.exit(1)
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()