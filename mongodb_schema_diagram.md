# 🗄️ Fashion Market Analyst - MongoDB Data Architecture

## 📍 **MongoDB Location & Setup**
```
🖥️  Host: localhost:27017
🗄️  Database: fashion_analyst
🔧 Connection: mongodb://localhost:27017/app_db (redirects to fashion_analyst)
📦 Total Size: 1,071,048 bytes (~1.07 MB)
📊 Documents: 2,956 total (2,746 mentions + 210 analytics)
```

## 🏗️ **Database Schema Architecture**

```
fashion_analyst (Database)
├── 📝 mentions (Collection)                    [2,746 documents]
│   ├── _id: ObjectId                          (MongoDB auto-generated)
│   ├── id: String (UUID)                      ✅ Our app ID
│   ├── brand: String                          👗 Brand name
│   ├── source: String                         🌐 reddit/news/social
│   ├── content: String                        💬 Mention text
│   ├── sentiment_score: Float                 😊 -1.0 to 1.0
│   ├── sentiment_label: String                🏷️ positive/negative/neutral
│   ├── engagement: Integer                    📊 likes/upvotes/shares
│   ├── timestamp: ISO String                  ⏰ UTC timestamp
│   └── url: String (Optional)                 🔗 Source URL
│
└── 📊 analytics (Collection)                   [210 documents]
    ├── _id: ObjectId                          (MongoDB auto-generated)
    ├── id: String (UUID)                      ✅ Our app ID
    ├── brand: String                          👗 Brand name
    ├── total_mentions: Integer                📝 Count of mentions
    ├── sentiment_avg: Float                   📈 Average sentiment
    ├── sentiment_trend: String                📊 rising/falling/stable
    ├── market_share_prediction: Float         💹 Predicted market share %
    ├── engagement_score: Integer              🔥 Total engagement
    └── timestamp: ISO String                  ⏰ UTC timestamp
```

## 📊 **Current Data Distribution**

### **Mentions by Brand** (Top brands by mention count):
```
W:              228 mentions  ████████████
AND:            228 mentions  ████████████
Myntra:         228 mentions  ████████████
Nike:           216 mentions  ███████████
Zara:           216 mentions  ███████████
H&M:            216 mentions  ███████████
Adidas:         194 mentions  ██████████
Uniqlo:         192 mentions  ██████████
Fabindia:       190 mentions  █████████
Ajio:           181 mentions  █████████
Forever 21:     181 mentions  █████████
Shein:          180 mentions  █████████
Nykaa Fashion:  152 mentions  ████████
Global Desi:    144 mentions  ███████
```

### **Mentions by Source**:
```
Social Media:   1,235 mentions  ████████████████████████████
Reddit API:       770 mentions  ██████████████████
News Data:        741 mentions  █████████████████
```

## 📋 **Sample JSON Documents**

### **Mentions Document Structure**:
```json
{
  "id": "1bf58540-5954-4f72-b108-6bbd3fa59961",
  "brand": "Myntra",
  "source": "reddit",
  "content": "This señorita brought the heat, margarita Speghetti top From SASSAFRAS ( Myntra)\nDenim jeans from Fabelly \nPink coloured mules from Steve Madden ",
  "sentiment_score": 0.2023,
  "sentiment_label": "positive",
  "engagement": 29,
  "timestamp": "2025-09-03T23:12:36.220376+00:00",
  "url": "https://reddit.com/r/fashion/comments/1mjyjuu/this_señorita_brought_the_heat_margarita/"
}
```

### **Analytics Document Structure**:
```json
{
  "id": "4cb45048-a032-489b-a04a-36a10ffe1bd4",
  "brand": "Myntra",
  "total_mentions": 12,
  "sentiment_avg": 0.103,
  "sentiment_trend": "rising",
  "market_share_prediction": 1.47,
  "engagement_score": 1042,
  "timestamp": "2025-09-03T23:12:42.493537+00:00"
}
```

## 🔄 **Data Flow Architecture**

```
                        🌐 DATA SOURCES
    ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
    │   Reddit API   │  │ Simulated News │  │ Social Media   │
    │   (Real Data)  │  │     Data       │  │   Simulation   │
    └────────────────┘  └────────────────┘  └────────────────┘
            │                    │                    │
            └────────────────────┼────────────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    🧠 VADER Sentiment   │
                    │       Analysis          │
                    │   (-1.0 to +1.0 scale)  │
                    └─────────────────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   📝 MongoDB mentions   │
                    │      Collection         │
                    │    (2,746 documents)    │
                    └─────────────────────────┘
                                 │
                                 ▼
           ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
           │ Sentiment   │  │ Market      │  │ Engagement  │
           │ Trend       │  │ Share       │  │ Scoring     │
           │ (ML Model)  │  │ Prediction  │  │ (Sum/Avg)   │
           └─────────────┘  └─────────────┘  └─────────────┘
                    │              │              │
                    └──────────────┼──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────┐
                    │  📊 MongoDB analytics   │
                    │      Collection         │
                    │    (210 documents)      │
                    └─────────────────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────┐
                    │   🚀 FastAPI Backend    │
                    │   /api/dashboard        │
                    │   /api/brands           │
                    │   /api/collect-data     │
                    └─────────────────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────┐
                    │   ⚛️ React Frontend     │
                    │   Real-time Dashboard   │
                    │   Auto-refresh (2min)   │
                    └─────────────────────────┘
```

## 🔧 **Key Technical Details**

### **Data Collection Frequency**:
- ⏰ Background collection: Every 5 minutes
- 🔄 Frontend refresh: Every 2 minutes
- 📊 Real-time updates via API calls

### **Storage Strategy**:
- 🆔 **UUIDs**: App-generated unique identifiers (not MongoDB ObjectIds)
- 📅 **Timestamps**: ISO format with UTC timezone
- 🗄️ **Collections**: Separate mentions (raw data) and analytics (processed data)

### **Data Processing Pipeline**:
1. **Collection**: Reddit API + simulated data
2. **Sentiment**: VADER analyzer scoring
3. **Storage**: Raw mentions in MongoDB
4. **Processing**: ML models for trends and predictions
5. **Analytics**: Aggregated data storage
6. **Serving**: FastAPI endpoints for dashboard

### **Brand Coverage**:
- 🇮🇳 **Indian Brands**: 7 brands (Myntra, Fabindia, W, AND, Nykaa Fashion, Ajio, Global Desi)
- 🌍 **Global Brands**: 7 brands (Zara, H&M, Nike, Adidas, Uniqlo, Forever 21, Shein)
- 📊 **Total**: 14 fashion brands tracked

## 📈 **Current Analytics Snapshot**

| Brand | Sentiment | Trend | Market Share | Total Mentions |
|-------|-----------|-------|--------------|----------------|
| Uniqlo | +0.193 | ↘️ | 15.58% | 12 |
| AND | +0.181 | ↘️ | 12.8% | 12 |
| Adidas | +0.174 | ➡️ | 9.15% | 12 |
| Nike | +0.078 | ↗️ | 11.56% | 12 |
| Zara | +0.201 | ↗️ | 9.59% | 12 |
| H&M | +0.006 | ➡️ | 11.16% | 12 |
| Myntra | +0.120 | ↗️ | 1.92% | 12 |

*↗️ Rising | ↘️ Falling | ➡️ Stable*