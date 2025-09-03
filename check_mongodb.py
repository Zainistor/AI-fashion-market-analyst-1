#!/usr/bin/env python3
"""
MongoDB Data Inspection Script
Shows the actual data structure and schema for Fashion Market Analyst
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import json
from datetime import datetime
import os

async def inspect_mongodb():
    print("🔍 Fashion Market Analyst - MongoDB Data Inspection")
    print("=" * 60)
    
    # Connect to MongoDB
    MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(MONGO_URL)
    db = client.fashion_analyst
    
    print(f"📍 MongoDB Location: {MONGO_URL}")
    print(f"🗄️  Database: fashion_analyst")
    print()
    
    # List all collections
    collections = await db.list_collection_names()
    print(f"📂 Collections Found: {collections}")
    print()
    
    # Check mentions collection
    print("=" * 60)
    print("📝 MENTIONS COLLECTION SCHEMA & DATA")
    print("=" * 60)
    
    mentions_count = await db.mentions.count_documents({})
    print(f"📊 Total Mentions: {mentions_count}")
    
    if mentions_count > 0:
        # Get sample mention
        sample_mention = await db.mentions.find_one()
        print("\n🔍 Sample Mention Document:")
        print("-" * 40)
        for key, value in sample_mention.items():
            if key == '_id':
                print(f"  {key}: {value} (MongoDB ObjectId)")
            else:
                print(f"  {key}: {value}")
        
        # Show mentions by brand
        print(f"\n📈 Mentions by Brand:")
        print("-" * 40)
        pipeline = [
            {"$group": {"_id": "$brand", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        brand_counts = []
        async for doc in db.mentions.aggregate(pipeline):
            brand_counts.append(doc)
        
        for brand_data in brand_counts:
            print(f"  {brand_data['_id']}: {brand_data['count']} mentions")
        
        # Show mentions by source
        print(f"\n🌐 Mentions by Source:")
        print("-" * 40)
        pipeline = [
            {"$group": {"_id": "$source", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        async for doc in db.mentions.aggregate(pipeline):
            print(f"  {doc['_id']}: {doc['count']} mentions")
    
    print("\n" + "=" * 60)
    print("📊 ANALYTICS COLLECTION SCHEMA & DATA")
    print("=" * 60)
    
    analytics_count = await db.analytics.count_documents({})
    print(f"📊 Total Analytics Records: {analytics_count}")
    
    if analytics_count > 0:
        # Get sample analytics
        sample_analytics = await db.analytics.find_one()
        print("\n🔍 Sample Analytics Document:")
        print("-" * 40)
        for key, value in sample_analytics.items():
            if key == '_id':
                print(f"  {key}: {value} (MongoDB ObjectId)")
            else:
                print(f"  {key}: {value}")
        
        # Show latest analytics for each brand
        print(f"\n📈 Latest Analytics by Brand:")
        print("-" * 40)
        brands = await db.analytics.distinct("brand")
        for brand in sorted(brands):
            latest = await db.analytics.find_one(
                {"brand": brand}, 
                sort=[("timestamp", -1)]
            )
            if latest:
                print(f"  {brand}:")
                print(f"    Sentiment: {latest['sentiment_avg']:.3f} ({latest['sentiment_trend']})")
                print(f"    Market Share: {latest['market_share_prediction']}%")
                print(f"    Mentions: {latest['total_mentions']}")
                print(f"    Engagement: {latest['engagement_score']}")
    
    print("\n" + "=" * 60)
    print("🏗️  DATABASE SCHEMA DIAGRAM")
    print("=" * 60)
    
    schema_diagram = """
    
    fashion_analyst (Database)
    ├── mentions (Collection)
    │   ├── _id: ObjectId (MongoDB auto-generated)
    │   ├── id: String (UUID - our app ID)
    │   ├── brand: String (Brand name)
    │   ├── source: String (reddit/news/social)
    │   ├── content: String (Mention text)
    │   ├── sentiment_score: Float (-1.0 to 1.0)
    │   ├── sentiment_label: String (positive/negative/neutral)
    │   ├── engagement: Integer (likes/upvotes/shares)
    │   ├── timestamp: ISO String (UTC timestamp)
    │   └── url: String (Optional - source URL)
    │
    └── analytics (Collection)
        ├── _id: ObjectId (MongoDB auto-generated)
        ├── id: String (UUID - our app ID)
        ├── brand: String (Brand name)
        ├── total_mentions: Integer (Count of mentions)
        ├── sentiment_avg: Float (Average sentiment score)
        ├── sentiment_trend: String (rising/falling/stable)
        ├── market_share_prediction: Float (Predicted market share %)
        ├── engagement_score: Integer (Total engagement)
        └── timestamp: ISO String (UTC timestamp)
    
    """
    print(schema_diagram)
    
    print("=" * 60)
    print("🔧 DATA FLOW ARCHITECTURE")
    print("=" * 60)
    
    data_flow = """
    
    1. DATA COLLECTION (Every 5 minutes)
       ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
       │   Reddit API    │    │  Simulated      │    │  Simulated      │
       │   (Real Data)   │    │  News Data      │    │  Social Data    │
       └─────────────────┘    └─────────────────┘    └─────────────────┘
                │                       │                       │
                └───────────────────────┼───────────────────────┘
                                        │
                                        ▼
                               ┌─────────────────┐
                               │ VADER Sentiment │
                               │    Analysis     │
                               └─────────────────┘
                                        │
                                        ▼
                               ┌─────────────────┐
                               │   MongoDB       │
                               │   mentions      │
                               │   Collection    │
                               └─────────────────┘
    
    2. ML PROCESSING
       ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
       │ Sentiment Trend │    │ Market Share    │    │  Engagement     │
       │ Forecasting     │    │ Prediction      │    │  Scoring        │
       │(Linear Regr.)   │    │(Weighted Calc.) │    │(Sum of values)  │
       └─────────────────┘    └─────────────────┘    └─────────────────┘
                │                       │                       │
                └───────────────────────┼───────────────────────┘
                                        │
                                        ▼
                               ┌─────────────────┐
                               │   MongoDB       │
                               │   analytics     │
                               │   Collection    │
                               └─────────────────┘
    
    3. API SERVING
                               ┌─────────────────┐
                               │   FastAPI       │
                               │   /api/...      │
                               └─────────────────┘
                                        │
                                        ▼
                               ┌─────────────────┐
                               │   React         │
                               │   Dashboard     │
                               └─────────────────┘
    
    """
    print(data_flow)
    
    # Close connection
    client.close()

if __name__ == "__main__":
    asyncio.run(inspect_mongodb())