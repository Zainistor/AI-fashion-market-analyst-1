from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os
from datetime import datetime, timezone
import asyncio
import praw
import pandas as pd
import numpy as np
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import uuid
import json
import random
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Fashion Market Analyst API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(MONGO_URL)
db = client.fashion_analyst

# Reddit API setup
REDDIT_CLIENT_ID = "ksZ778g1MAoGFRUHuJxC9w"
REDDIT_CLIENT_SECRET = "Gy7vQdgPR5RipWrDfLGODIHwZ_6sxg"

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent="FashionAnalyst/1.0"
)

# Sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Fashion brands to track
BRANDS = {
    "indian": ["Myntra", "Fabindia", "W", "AND", "Nykaa Fashion", "Ajio", "Global Desi"],
    "global": ["Zara", "H&M", "Nike", "Adidas", "Uniqlo", "Forever 21", "Shein"]
}

ALL_BRANDS = BRANDS["indian"] + BRANDS["global"]

# Pydantic models
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

# Data collection functions
async def collect_reddit_mentions(brand: str, limit: int = 10):
    """Collect brand mentions from Reddit"""
    mentions = []
    try:
        # Search multiple subreddits for brand mentions
        subreddits = ["fashion", "malefashionadvice", "femalefashionadvice", "streetwear", "india", "IndiaInvestments"]
        
        for subreddit_name in subreddits[:2]:  # Limit to avoid rate limits
            try:
                subreddit = reddit.subreddit(subreddit_name)
                for submission in subreddit.search(brand, limit=limit//2):
                    # Analyze sentiment
                    text = f"{submission.title} {submission.selftext}"
                    sentiment = analyzer.polarity_scores(text)
                    
                    mention = BrandMention(
                        brand=brand,
                        source="reddit",
                        content=text[:500],  # Limit content length
                        sentiment_score=sentiment['compound'],
                        sentiment_label=get_sentiment_label(sentiment['compound']),
                        engagement=submission.score + submission.num_comments,
                        timestamp=datetime.now(timezone.utc).isoformat(),
                        url=f"https://reddit.com{submission.permalink}"
                    )
                    mentions.append(mention)
            except Exception as e:
                logger.error(f"Error collecting from subreddit {subreddit_name}: {e}")
                continue
                
    except Exception as e:
        logger.error(f"Error collecting Reddit mentions for {brand}: {e}")
    
    return mentions

def generate_simulated_news(brand: str, count: int = 5):
    """Generate simulated news mentions for brands"""
    news_templates = [
        f"{brand} launches new sustainable fashion line",
        f"{brand} reports strong quarterly growth in fashion segment",
        f"{brand} collaborates with leading designers for exclusive collection",
        f"{brand} expands digital presence with new mobile app features",
        f"{brand} introduces AI-powered personal styling recommendations",
        f"{brand} announces expansion to new international markets",
        f"{brand} receives award for innovative fashion technology"
    ]
    
    mentions = []
    for i in range(count):
        template = random.choice(news_templates)
        sentiment_score = random.uniform(-0.5, 0.8)  # Slightly positive bias for news
        
        mention = BrandMention(
            brand=brand,
            source="news",
            content=template,
            sentiment_score=sentiment_score,
            sentiment_label=get_sentiment_label(sentiment_score),
            engagement=random.randint(50, 500),
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        mentions.append(mention)
    
    return mentions

def generate_social_mentions(brand: str, count: int = 8):
    """Generate simulated social media mentions"""
    social_templates = [
        f"Just bought from {brand} and loving the quality! 😍",
        f"{brand} has the best customer service ever! Highly recommend",
        f"Not impressed with {brand}'s latest collection tbh",
        f"{brand} sale is live! Great deals on everything 🛍️",
        f"Why is {brand} so expensive? Looking for alternatives",
        f"{brand} fits perfectly! Will definitely shop again",
        f"Waiting for {brand} to restock my favorite items",
        f"{brand} delivery was super fast! Impressed 📦"
    ]
    
    mentions = []
    for i in range(count):
        template = random.choice(social_templates)
        sentiment_score = random.uniform(-0.8, 0.9)
        
        mention = BrandMention(
            brand=brand,
            source="social",
            content=template,
            sentiment_score=sentiment_score,
            sentiment_label=get_sentiment_label(sentiment_score),
            engagement=random.randint(10, 200),
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        mentions.append(mention)
    
    return mentions

def get_sentiment_label(score: float) -> str:
    """Convert sentiment score to label"""
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"

def predict_sentiment_trend(brand_mentions: List[BrandMention]) -> str:
    """Predict sentiment trend using simple linear regression"""
    if len(brand_mentions) < 3:
        return "stable"
    
    # Sort by timestamp and take recent mentions
    sorted_mentions = sorted(brand_mentions, key=lambda x: x.timestamp)[-10:]
    
    if len(sorted_mentions) < 3:
        return "stable"
    
    X = np.array(range(len(sorted_mentions))).reshape(-1, 1)
    y = np.array([m.sentiment_score for m in sorted_mentions])
    
    model = LinearRegression()
    model.fit(X, y)
    
    slope = model.coef_[0]
    
    if slope > 0.01:
        return "rising"
    elif slope < -0.01:
        return "falling"
    else:
        return "stable"

def predict_market_share(brand: str, all_mentions: List[BrandMention]) -> float:
    """Predict market share based on mention volume and engagement"""
    brand_mentions = [m for m in all_mentions if m.brand == brand]
    
    if not brand_mentions:
        return 0.0
    
    # Calculate weighted score based on mentions and engagement
    total_score = sum(m.engagement * (1 + m.sentiment_score) for m in brand_mentions)
    all_scores = sum(m.engagement * (1 + m.sentiment_score) for m in all_mentions)
    
    if all_scores == 0:
        return 0.0
    
    market_share = (total_score / all_scores) * 100
    return round(market_share, 2)

# API Routes
@app.get("/")
async def root():
    return {"message": "Fashion Market Analyst API", "status": "running"}

@app.get("/api/")
async def api_root():
    return {"message": "Fashion Market Analyst API", "status": "running"}

@app.post("/api/collect-data")
async def collect_data():
    """Collect data for all brands and store in database"""
    try:
        all_mentions = []
        
        for brand in ALL_BRANDS:
            logger.info(f"Collecting data for {brand}")
            
            # Collect from different sources
            reddit_mentions = await collect_reddit_mentions(brand, limit=5)
            news_mentions = generate_simulated_news(brand, count=3)
            social_mentions = generate_social_mentions(brand, count=5)
            
            brand_mentions = reddit_mentions + news_mentions + social_mentions
            all_mentions.extend(brand_mentions)
            
            # Store mentions in database
            for mention in brand_mentions:
                await db.mentions.insert_one(mention.dict())
        
        # Generate analytics for each brand
        for brand in ALL_BRANDS:
            brand_mentions = [m for m in all_mentions if m.brand == brand]
            
            if brand_mentions:
                avg_sentiment = sum(m.sentiment_score for m in brand_mentions) / len(brand_mentions)
                trend = predict_sentiment_trend(brand_mentions)
                market_share = predict_market_share(brand, all_mentions)
                total_engagement = sum(m.engagement for m in brand_mentions)
                
                analytics = BrandAnalytics(
                    brand=brand,
                    total_mentions=len(brand_mentions),
                    sentiment_avg=round(avg_sentiment, 3),
                    sentiment_trend=trend,
                    market_share_prediction=market_share,
                    engagement_score=total_engagement,
                    timestamp=datetime.now(timezone.utc).isoformat()
                )
                
                await db.analytics.insert_one(analytics.dict())
        
        return {"message": f"Data collected for {len(ALL_BRANDS)} brands", "total_mentions": len(all_mentions)}
        
    except Exception as e:
        logger.error(f"Error collecting data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dashboard", response_model=DashboardData)
async def get_dashboard_data():
    """Get comprehensive dashboard data"""
    try:
        # Get latest analytics for each brand
        brands_overview = []
        sentiment_trends = {}
        market_predictions = {}
        
        for brand in ALL_BRANDS:
            # Get latest analytics
            latest_analytics = await db.analytics.find_one(
                {"brand": brand}, 
                sort=[("timestamp", -1)]
            )
            
            if latest_analytics:
                brands_overview.append({
                    "brand": brand,
                    "sentiment_avg": latest_analytics["sentiment_avg"],
                    "sentiment_trend": latest_analytics["sentiment_trend"],
                    "total_mentions": latest_analytics["total_mentions"],
                    "engagement_score": latest_analytics["engagement_score"],
                    "market_share": latest_analytics["market_share_prediction"]
                })
                
                # Get sentiment trend data (last 10 analytics entries)
                trend_data = await db.analytics.find(
                    {"brand": brand}, 
                    sort=[("timestamp", -1)], 
                    limit=10
                ).to_list(length=10)
                
                sentiment_trends[brand] = [item["sentiment_avg"] for item in reversed(trend_data)]
                market_predictions[brand] = latest_analytics["market_share_prediction"]
        
        # Get recent mentions
        recent_mentions_cursor = db.mentions.find(
            {}, 
            sort=[("timestamp", -1)], 
            limit=20
        )
        recent_mentions = await recent_mentions_cursor.to_list(length=20)
        
        # Convert to BrandMention objects
        recent_mentions_obj = [BrandMention(**mention) for mention in recent_mentions]
        
        dashboard_data = DashboardData(
            brands_overview=brands_overview,
            sentiment_trends=sentiment_trends,
            market_predictions=market_predictions,
            recent_mentions=recent_mentions_obj,
            last_updated=datetime.now(timezone.utc).isoformat()
        )
        
        return dashboard_data
        
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/brands")
async def get_brands():
    """Get list of all tracked brands"""
    return {"brands": BRANDS, "total_brands": len(ALL_BRANDS)}

@app.get("/api/brand/{brand_name}/analytics")
async def get_brand_analytics(brand_name: str):
    """Get detailed analytics for a specific brand"""
    try:
        # Get recent analytics
        analytics_cursor = db.analytics.find(
            {"brand": brand_name}, 
            sort=[("timestamp", -1)], 
            limit=30
        )
        analytics = await analytics_cursor.to_list(length=30)
        
        # Get recent mentions
        mentions_cursor = db.mentions.find(
            {"brand": brand_name}, 
            sort=[("timestamp", -1)], 
            limit=50
        )
        mentions = await mentions_cursor.to_list(length=50)
        
        return {
            "brand": brand_name,
            "analytics_history": analytics,
            "recent_mentions": mentions,
            "total_analytics": len(analytics),
            "total_mentions": len(mentions)
        }
        
    except Exception as e:
        logger.error(f"Error getting brand analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Background task for continuous data collection
async def continuous_data_collection():
    """Background task to collect data every 5 minutes"""
    while True:
        try:
            logger.info("Starting background data collection...")
            await collect_data()
            logger.info("Background data collection completed")
            await asyncio.sleep(300)  # Wait 5 minutes
        except Exception as e:
            logger.error(f"Error in background data collection: {e}")
            await asyncio.sleep(60)  # Wait 1 minute before retrying

@app.on_event("startup")
async def startup_event():
    """Start background tasks on startup"""
    logger.info("Starting Fashion Market Analyst API...")
    # Start background data collection
    asyncio.create_task(continuous_data_collection())
    logger.info("Background data collection started")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)