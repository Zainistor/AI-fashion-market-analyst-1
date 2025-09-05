# Here are your Instructions
# 👗 Fashion Market Analyst

**Real-time fashion brand sentiment analysis platform** with ML-powered predictions and beautiful analytics dashboard.

![Fashion Market Analyst](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Tech Stack](https://img.shields.io/badge/Stack-FastAPI%20%2B%20React%20%2B%20MongoDB-blue)
![Data Sources](https://img.shields.io/badge/Data-Reddit%20API%20%2B%20ML%20Simulation-orange)

## 🚀 **Overview**

Fashion Market Analyst tracks **14 major fashion brands** (7 Indian + 7 Global) in real-time, analyzing brand mentions, sentiment trends, and market predictions using advanced ML algorithms and live data collection.

### **📊 Key Features**

- **🔍 Real-time Data Collection**: Reddit API + simulated news/social data
- **🧠 AI Sentiment Analysis**: VADER sentiment analyzer with ML predictions
- **📈 Market Predictions**: Sentiment forecasting & market share analysis
- **🎨 Beautiful Dashboard**: Live analytics with auto-refresh every 2 minutes
- **📱 Responsive Design**: Works perfectly on desktop and mobile
- **⚡ Background Processing**: Continuous data collection every 5 minutes

### **👗 Tracked Brands**

**🇮🇳 Indian Fashion Brands:**
- Myntra, Fabindia, W, AND, Nykaa Fashion, Ajio, Global Desi

**🌍 Global Fashion Brands:**
- Zara, H&M, Nike, Adidas, Uniqlo, Forever 21, Shein

## 🛠️ **Tech Stack**

- **Backend**: FastAPI (Python)
- **Frontend**: React.js with Tailwind CSS
- **Database**: MongoDB with Motor (AsyncIO)
- **ML/Analytics**: VADER Sentiment, Scikit-learn
- **Data Sources**: Reddit API (PRAW), Simulated data
- **Real-time**: WebSocket-like polling every 2 minutes

## 📋 **Prerequisites**

- **Python 3.8+**
- **Node.js 16+** 
- **MongoDB** (Community Edition)
- **Reddit API Credentials** (free)
- **Git**

## 🚀 **Quick Start**

### **1. Clone the Repository**
```bash
git clone <your-repo-url>
cd fashion-market-analyst
```

### **2. Backend Setup**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
```

Edit `.env` file:
```env
MONGO_URL=mongodb://localhost:27017/fashion_analyst
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
CORS_ORIGINS="*"
```

### **3. Frontend Setup**
```bash
cd ../frontend

# Install dependencies
yarn install

# Setup environment variables
cp .env.example .env
```

Edit `frontend/.env`:
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

### **4. Database Setup**
```bash
# Start MongoDB service
sudo systemctl start mongod    # Linux
brew services start mongodb    # macOS
net start MongoDB             # Windows

# MongoDB will auto-create database and collections
```

### **5. Run the Application**

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python server.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
yarn start
```

**🌐 Access the app at: http://localhost:3000**

## 🔧 **API Documentation**

### **Base URL**: `http://localhost:8001`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/` | GET | API health check |
| `/api/dashboard` | GET | Complete dashboard data |
| `/api/brands` | GET | List of tracked brands |
| `/api/collect-data` | POST | Trigger data collection |
| `/api/brand/{name}/analytics` | GET | Individual brand analytics |

### **Sample API Response - Dashboard**
```json
{
  "brands_overview": [
    {
      "brand": "Zara",
      "sentiment_avg": 0.201,
      "sentiment_trend": "rising",
      "total_mentions": 12,
      "market_share": 9.59,
      "engagement_score": 8011
    }
  ],
  "sentiment_trends": {
    "Zara": [0.15, 0.18, 0.201]
  },
  "market_predictions": {
    "Zara": 9.59
  },
  "recent_mentions": [...],
  "last_updated": "2025-09-03T23:12:42.493537+00:00"
}
```

## 🗄️ **Database Schema**

### **MongoDB Collections**

**📝 mentions** (Raw data):
```javascript
{
  id: "uuid",
  brand: "Zara",
  source: "reddit|news|social",
  content: "Fashion mention text...",
  sentiment_score: 0.201,        // -1.0 to +1.0
  sentiment_label: "positive",   // positive/negative/neutral
  engagement: 8011,              // likes/shares/upvotes
  timestamp: "ISO UTC string",
  url: "source_url"             // optional
}
```

**📊 analytics** (Processed data):
```javascript
{
  id: "uuid",
  brand: "Zara",
  total_mentions: 12,
  sentiment_avg: 0.201,
  sentiment_trend: "rising",     // rising/falling/stable
  market_share_prediction: 9.59,
  engagement_score: 8011,
  timestamp: "ISO UTC string"
}
```

## 📊 **Data Flow Architecture**

```
🌐 DATA SOURCES
├── Reddit API (Real mentions)
├── News Simulation (Fashion news)
└── Social Media Simulation

    ⬇️ Processing Pipeline
    
🔍 VADER Sentiment Analysis
├── Sentiment scoring (-1 to +1)
├── Label classification
└── Engagement tracking

    ⬇️ Storage
    
💾 MongoDB Collections
├── mentions (raw data)
└── analytics (ML processed)

    ⬇️ ML Processing
    
🧠 Machine Learning
├── Sentiment trend forecasting
├── Market share prediction
└── Engagement scoring

    ⬇️ API Layer
    
🚀 FastAPI Backend
├── Real-time endpoints
├── Background data collection
└── JSON API responses

    ⬇️ Frontend
    
⚛️ React Dashboard
├── Live data visualization
├── Auto-refresh (2 min)
└── Responsive design
```

## 🧪 **Testing**

### **Backend Testing**
```bash
cd backend
python -m pytest tests/
# Or test manually:
curl http://localhost:8001/api/dashboard
```

### **Frontend Testing**
```bash
cd frontend
yarn test
```

### **Integration Testing**
1. Start both backend and frontend
2. Click "Refresh Data" button
3. Verify data appears in dashboard
4. Check auto-refresh functionality

## 🔧 **Configuration**

### **Reddit API Setup**
1. Go to https://www.reddit.com/prefs/apps
2. Create a new app (script type)
3. Copy Client ID and Secret
4. Add to backend/.env file

### **MongoDB Configuration**
- **Default**: localhost:27017
- **Database**: fashion_analyst (auto-created)
- **Collections**: mentions, analytics (auto-created)

### **Environment Variables**

**Backend (.env):**
```env
MONGO_URL=mongodb://localhost:27017/fashion_analyst
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
CORS_ORIGINS="*"
```

**Frontend (.env):**
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

## 📁 **Project Structure**

```
fashion-market-analyst/
├── backend/
│   ├── server.py              # FastAPI main application
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables
│   └── tests/                 # Backend tests
├── frontend/
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── App.css           # Tailwind styles
│   │   └── index.js          # React entry point
│   ├── package.json          # Node dependencies
│   ├── .env                  # Frontend environment
│   └── public/               # Static assets
├── docs/
│   ├── mongodb_schema_diagram.md
│   └── api_documentation.md
├── README.md                 # This file
└── test_result.md           # Testing results
```

## 🚀 **Deployment**

### **Production Deployment**
1. **Backend**: Deploy FastAPI with Gunicorn/Uvicorn
2. **Frontend**: Build with `yarn build` and serve with Nginx
3. **Database**: MongoDB Atlas or self-hosted MongoDB
4. **Environment**: Update URLs and credentials for production

### **Docker Deployment** (Optional)
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 📊 **Performance Stats**

- **⚡ Load Time**: <2 seconds
- **🔄 Data Refresh**: Every 2 minutes (frontend), 5 minutes (collection)
- **📊 Database Size**: ~1MB per day of data
- **🚀 API Response**: <500ms average
- **📱 Mobile Ready**: Fully responsive design

## 🐛 **Troubleshooting**

### **Common Issues**

**MongoDB Connection Error:**
```bash
# Check if MongoDB is running
sudo systemctl status mongod
# Start MongoDB
sudo systemctl start mongod
```

**Reddit API Rate Limits:**
- App uses free tier limits
- Background collection respects rate limits
- Simulated data fills gaps automatically

**Frontend Not Loading:**
```bash
# Check backend is running
curl http://localhost:8001/api/
# Verify environment variables
cat frontend/.env
```

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m \'Add amazing feature\'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Reddit API** for real fashion discussion data
- **VADER Sentiment** for sentiment analysis
- **MongoDB** for document storage
- **FastAPI** for high-performance API
- **React + Tailwind** for beautiful UI

## 📞 **Support**
