#!/usr/bin/env python3
"""
Show actual JSON structure of MongoDB documents
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import json
from datetime import datetime
import os

async def show_json_structure():
    print("📋 Fashion Market Analyst - JSON Document Structure")
    print("=" * 70)
    
    # Connect to MongoDB
    MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(MONGO_URL)
    db = client.fashion_analyst
    
    # Get sample mention
    mention = await db.mentions.find_one()
    if mention:
        print("📝 MENTIONS COLLECTION - Sample Document (JSON):")
        print("-" * 70)
        # Remove MongoDB ObjectId for clean JSON
        mention_clean = {k: v for k, v in mention.items() if k != '_id'}
        print(json.dumps(mention_clean, indent=2, default=str))
    
    print("\n" + "=" * 70)
    
    # Get sample analytics
    analytics = await db.analytics.find_one()
    if analytics:
        print("📊 ANALYTICS COLLECTION - Sample Document (JSON):")
        print("-" * 70)
        # Remove MongoDB ObjectId for clean JSON
        analytics_clean = {k: v for k, v in analytics.items() if k != '_id'}
        print(json.dumps(analytics_clean, indent=2, default=str))
    
    print("\n" + "=" * 70)
    print("🔍 PYDANTIC MODELS USED IN CODE:")
    print("-" * 70)
    
    pydantic_models = '''
class BrandMention(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    brand: str
    source: str  # reddit, news, social
    content: str
    sentiment_score: float
    sentiment_label: str  # positive, negative, neutral
    engagement: int  # likes, upvotes, shares
    timestamp: str
    url: Optional[str] = None

class BrandAnalytics(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    brand: str
    total_mentions: int
    sentiment_avg: float
    sentiment_trend: str  # rising, falling, stable
    market_share_prediction: float
    engagement_score: int
    timestamp: str

class DashboardData(BaseModel):
    brands_overview: List[Dict[str, Any]]
    sentiment_trends: Dict[str, List[float]]
    market_predictions: Dict[str, float]
    recent_mentions: List[BrandMention]
    last_updated: str
'''
    print(pydantic_models)
    
    # Show database size info
    print("\n" + "=" * 70)
    print("📊 DATABASE STATISTICS:")
    print("-" * 70)
    
    mentions_count = await db.mentions.count_documents({})
    analytics_count = await db.analytics.count_documents({})
    
    # Get database stats
    stats = await db.command("dbstats")
    
    print(f"📝 Mentions Documents: {mentions_count:,}")
    print(f"📊 Analytics Documents: {analytics_count:,}")
    print(f"💾 Total Database Size: {stats.get('dataSize', 0):,} bytes")
    print(f"📦 Storage Size: {stats.get('storageSize', 0):,} bytes")
    print(f"🗂️  Collections: {stats.get('collections', 0)}")
    print(f"📑 Indexes: {stats.get('indexes', 0)}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(show_json_structure())