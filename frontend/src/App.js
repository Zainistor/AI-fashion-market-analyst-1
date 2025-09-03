import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// Get backend URL from environment
const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

function App() {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedBrand, setSelectedBrand] = useState(null);
  const [brands, setBrands] = useState({ indian: [], global: [] });
  const [isCollecting, setIsCollecting] = useState(false);

  // Fetch dashboard data
  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/api/dashboard`);
      setDashboardData(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
      setError('Failed to fetch dashboard data');
    } finally {
      setLoading(false);
    }
  };

  // Fetch brands list
  const fetchBrands = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/brands`);
      setBrands(response.data.brands);
    } catch (err) {
      console.error('Error fetching brands:', err);
    }
  };

  // Trigger data collection
  const triggerDataCollection = async () => {
    try {
      setIsCollecting(true);
      await axios.post(`${API_BASE_URL}/api/collect-data`);
      // Refresh dashboard after collection
      setTimeout(fetchDashboardData, 2000);
    } catch (err) {
      console.error('Error triggering data collection:', err);
      setError('Failed to collect data');
    } finally {
      setIsCollecting(false);
    }
  };

  useEffect(() => {
    fetchBrands();
    fetchDashboardData();
    
    // Set up automatic refresh every 2 minutes
    const interval = setInterval(fetchDashboardData, 120000);
    return () => clearInterval(interval);
  }, []);

  const getSentimentColor = (score) => {
    if (score >= 0.1) return 'text-green-600';
    if (score <= -0.1) return 'text-red-600';
    return 'text-yellow-600';
  };

  const getSentimentBg = (score) => {
    if (score >= 0.1) return 'bg-green-100';
    if (score <= -0.1) return 'bg-red-100';
    return 'bg-yellow-100';
  };

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'rising': return '📈';
      case 'falling': return '📉';
      default: return '➡️';
    }
  };

  if (loading && !dashboardData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading fashion market data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50">
      {/* Header */}
      <header className="bg-white shadow-lg border-b-4 border-purple-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="bg-gradient-to-r from-purple-600 to-pink-600 p-3 rounded-full">
                <span className="text-white font-bold text-xl">👗</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Fashion Market Analyst</h1>
                <p className="text-sm text-gray-600">Real-time brand sentiment & market predictions</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={triggerDataCollection}
                disabled={isCollecting}
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  isCollecting 
                    ? 'bg-gray-400 cursor-not-allowed' 
                    : 'bg-purple-600 hover:bg-purple-700 text-white shadow-lg hover:shadow-xl'
                }`}
              >
                {isCollecting ? '🔄 Collecting...' : '📊 Refresh Data'}
              </button>
              {dashboardData && (
                <span className="text-sm text-gray-500">
                  Last updated: {new Date(dashboardData.last_updated).toLocaleTimeString()}
                </span>
              )}
            </div>
          </div>
        </div>
      </header>

      {error && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-4">
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        </div>
      )}

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!dashboardData || dashboardData.brands_overview.length === 0 ? (
          <div className="text-center py-16">
            <div className="bg-white rounded-xl shadow-lg p-8 max-w-md mx-auto">
              <div className="text-6xl mb-4">📊</div>
              <h2 className="text-xl font-semibold text-gray-900 mb-2">No Data Available</h2>
              <p className="text-gray-600 mb-6">Click "Refresh Data" to start collecting fashion market insights</p>
              <button
                onClick={triggerDataCollection}
                disabled={isCollecting}
                className="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition-colors font-medium"
              >
                {isCollecting ? '🔄 Collecting Data...' : '🚀 Start Analysis'}
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-8">
            {/* Overview Stats */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Total Brands</p>
                    <p className="text-3xl font-bold text-gray-900">{dashboardData.brands_overview.length}</p>
                  </div>
                  <div className="bg-purple-100 p-3 rounded-full">
                    <span className="text-2xl">🏷️</span>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Total Mentions</p>
                    <p className="text-3xl font-bold text-gray-900">
                      {dashboardData.brands_overview.reduce((sum, brand) => sum + brand.total_mentions, 0)}
                    </p>
                  </div>
                  <div className="bg-blue-100 p-3 rounded-full">
                    <span className="text-2xl">💬</span>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Positive Sentiment</p>
                    <p className="text-3xl font-bold text-green-600">
                      {dashboardData.brands_overview.filter(b => b.sentiment_avg > 0.1).length}
                    </p>
                  </div>
                  <div className="bg-green-100 p-3 rounded-full">
                    <span className="text-2xl">😊</span>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Rising Trends</p>
                    <p className="text-3xl font-bold text-purple-600">
                      {dashboardData.brands_overview.filter(b => b.sentiment_trend === 'rising').length}
                    </p>
                  </div>
                  <div className="bg-purple-100 p-3 rounded-full">
                    <span className="text-2xl">📈</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Brand Categories */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Indian Brands */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
                  <span className="mr-2">🇮🇳</span>
                  Indian Fashion Brands
                </h2>
                <div className="space-y-4">
                  {dashboardData.brands_overview
                    .filter(brand => brands.indian.includes(brand.brand))
                    .map((brand, index) => (
                      <div key={index} className={`p-4 rounded-lg border-2 ${getSentimentBg(brand.sentiment_avg)} border-opacity-20`}>
                        <div className="flex justify-between items-start mb-2">
                          <h3 className="font-semibold text-gray-900">{brand.brand}</h3>
                          <span className="text-lg">{getTrendIcon(brand.sentiment_trend)}</span>
                        </div>
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div>
                            <span className="text-gray-600">Sentiment: </span>
                            <span className={`font-medium ${getSentimentColor(brand.sentiment_avg)}`}>
                              {brand.sentiment_avg > 0 ? '+' : ''}{brand.sentiment_avg.toFixed(3)}
                            </span>
                          </div>
                          <div>
                            <span className="text-gray-600">Mentions: </span>
                            <span className="font-medium">{brand.total_mentions}</span>
                          </div>
                          <div>
                            <span className="text-gray-600">Market Share: </span>
                            <span className="font-medium text-purple-600">{brand.market_share}%</span>
                          </div>
                          <div>
                            <span className="text-gray-600">Engagement: </span>
                            <span className="font-medium">{brand.engagement_score}</span>
                          </div>
                        </div>
                      </div>
                    ))}
                </div>
              </div>

              {/* Global Brands */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
                  <span className="mr-2">🌍</span>
                  Global Fashion Brands
                </h2>
                <div className="space-y-4">
                  {dashboardData.brands_overview
                    .filter(brand => brands.global.includes(brand.brand))
                    .map((brand, index) => (
                      <div key={index} className={`p-4 rounded-lg border-2 ${getSentimentBg(brand.sentiment_avg)} border-opacity-20`}>
                        <div className="flex justify-between items-start mb-2">
                          <h3 className="font-semibold text-gray-900">{brand.brand}</h3>
                          <span className="text-lg">{getTrendIcon(brand.sentiment_trend)}</span>
                        </div>
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div>
                            <span className="text-gray-600">Sentiment: </span>
                            <span className={`font-medium ${getSentimentColor(brand.sentiment_avg)}`}>
                              {brand.sentiment_avg > 0 ? '+' : ''}{brand.sentiment_avg.toFixed(3)}
                            </span>
                          </div>
                          <div>
                            <span className="text-gray-600">Mentions: </span>
                            <span className="font-medium">{brand.total_mentions}</span>
                          </div>
                          <div>
                            <span className="text-gray-600">Market Share: </span>
                            <span className="font-medium text-purple-600">{brand.market_share}%</span>
                          </div>
                          <div>
                            <span className="text-gray-600">Engagement: </span>
                            <span className="font-medium">{brand.engagement_score}</span>
                          </div>
                        </div>
                      </div>
                    ))}
                </div>
              </div>
            </div>

            {/* Recent Mentions */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
                <span className="mr-2">💬</span>
                Recent Brand Mentions
              </h2>
              <div className="space-y-4 max-h-96 overflow-y-auto">
                {dashboardData.recent_mentions.slice(0, 10).map((mention, index) => (
                  <div key={index} className="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg">
                    <div className="flex-shrink-0">
                      <div className={`w-3 h-3 rounded-full ${
                        mention.sentiment_label === 'positive' ? 'bg-green-500' :
                        mention.sentiment_label === 'negative' ? 'bg-red-500' : 'bg-yellow-500'
                      }`}></div>
                    </div>
                    <div className="flex-grow">
                      <div className="flex justify-between items-start">
                        <div>
                          <span className="font-medium text-gray-900">{mention.brand}</span>
                          <span className="ml-2 text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded-full">
                            {mention.source}
                          </span>
                        </div>
                        <span className="text-xs text-gray-500">
                          {new Date(mention.timestamp).toLocaleTimeString()}
                        </span>
                      </div>
                      <p className="text-sm text-gray-700 mt-1">{mention.content}</p>
                      <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                        <span>Sentiment: {mention.sentiment_score.toFixed(3)}</span>
                        <span>Engagement: {mention.engagement}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;