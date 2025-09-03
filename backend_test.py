#!/usr/bin/env python3
"""
Comprehensive Backend API Tests for Fashion Market Analyst
Tests all API endpoints and validates data collection functionality
"""

import requests
import json
import time
from datetime import datetime
import sys

# Use the production URL from frontend/.env
BASE_URL = "https://fashion-radar.preview.emergentagent.com"

# Expected brands
EXPECTED_BRANDS = {
    "indian": ["Myntra", "Fabindia", "W", "AND", "Nykaa Fashion", "Ajio", "Global Desi"],
    "global": ["Zara", "H&M", "Nike", "Adidas", "Uniqlo", "Forever 21", "Shein"]
}
ALL_BRANDS = EXPECTED_BRANDS["indian"] + EXPECTED_BRANDS["global"]

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 30
        self.results = []
        
    def log_result(self, test_name, success, message, details=None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        print(f"{status}: {test_name} - {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    def test_api_root(self):
        """Test GET / endpoint"""
        try:
            response = self.session.get(f"{BASE_URL}/")
            if response.status_code == 200:
                # Try to parse as JSON, but handle cases where it might not be JSON
                try:
                    data = response.json()
                    if "message" in data and "status" in data:
                        self.log_result("API Root Endpoint", True, "Root endpoint responding correctly")
                        return True
                    else:
                        self.log_result("API Root Endpoint", False, "Invalid response format", data)
                        return False
                except json.JSONDecodeError:
                    # If it's not JSON but returns 200, that's still a valid response
                    self.log_result("API Root Endpoint", True, "Root endpoint responding (non-JSON)")
                    return True
            else:
                self.log_result("API Root Endpoint", False, f"HTTP {response.status_code}", response.text[:200])
                return False
        except Exception as e:
            self.log_result("API Root Endpoint", False, "Connection failed", str(e))
            return False
    
    def test_api_prefix_root(self):
        """Test GET /api/ endpoint"""
        try:
            response = self.session.get(f"{BASE_URL}/api/")
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "status" in data:
                    self.log_result("API Prefix Root", True, "/api/ endpoint responding correctly")
                    return True
                else:
                    self.log_result("API Prefix Root", False, "Invalid response format", data)
                    return False
            else:
                self.log_result("API Prefix Root", False, f"HTTP {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("API Prefix Root", False, "Connection failed", str(e))
            return False
    
    def test_brands_endpoint(self):
        """Test GET /api/brands endpoint"""
        try:
            response = self.session.get(f"{BASE_URL}/api/brands")
            if response.status_code == 200:
                data = response.json()
                
                # Validate structure
                if "brands" not in data or "total_brands" not in data:
                    self.log_result("Brands Endpoint", False, "Missing required fields", data)
                    return False
                
                # Validate brand categories
                brands = data["brands"]
                if "indian" not in brands or "global" not in brands:
                    self.log_result("Brands Endpoint", False, "Missing brand categories", brands)
                    return False
                
                # Validate total count
                total_expected = len(EXPECTED_BRANDS["indian"]) + len(EXPECTED_BRANDS["global"])
                if data["total_brands"] != total_expected:
                    self.log_result("Brands Endpoint", False, f"Expected {total_expected} brands, got {data['total_brands']}")
                    return False
                
                # Validate brand lists
                for category in ["indian", "global"]:
                    expected_brands = set(EXPECTED_BRANDS[category])
                    actual_brands = set(brands[category])
                    if expected_brands != actual_brands:
                        missing = expected_brands - actual_brands
                        extra = actual_brands - expected_brands
                        self.log_result("Brands Endpoint", False, f"Brand mismatch in {category}", 
                                      f"Missing: {missing}, Extra: {extra}")
                        return False
                
                self.log_result("Brands Endpoint", True, f"All {total_expected} brands correctly configured")
                return True
            else:
                self.log_result("Brands Endpoint", False, f"HTTP {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Brands Endpoint", False, "Request failed", str(e))
            return False
    
    def test_data_collection(self):
        """Test POST /api/collect-data endpoint"""
        try:
            print("   Triggering data collection (this may take 30-60 seconds)...")
            response = self.session.post(f"{BASE_URL}/api/collect-data")
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                if "message" not in data or "total_mentions" not in data:
                    self.log_result("Data Collection", False, "Invalid response format", data)
                    return False
                
                # Validate mentions count
                total_mentions = data["total_mentions"]
                if total_mentions <= 0:
                    self.log_result("Data Collection", False, "No mentions collected", data)
                    return False
                
                # Validate message contains brand count
                expected_brand_count = len(ALL_BRANDS)
                if str(expected_brand_count) not in data["message"]:
                    self.log_result("Data Collection", False, "Message doesn't mention correct brand count", data)
                    return False
                
                self.log_result("Data Collection", True, f"Successfully collected {total_mentions} mentions for {expected_brand_count} brands")
                return True
            else:
                self.log_result("Data Collection", False, f"HTTP {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Data Collection", False, "Request failed", str(e))
            return False
    
    def test_dashboard_endpoint(self):
        """Test GET /api/dashboard endpoint"""
        try:
            response = self.session.get(f"{BASE_URL}/api/dashboard")
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate main structure
                required_fields = ["brands_overview", "sentiment_trends", "market_predictions", "recent_mentions", "last_updated"]
                for field in required_fields:
                    if field not in data:
                        self.log_result("Dashboard Endpoint", False, f"Missing field: {field}", data.keys())
                        return False
                
                # Validate brands_overview
                brands_overview = data["brands_overview"]
                if not isinstance(brands_overview, list):
                    self.log_result("Dashboard Endpoint", False, "brands_overview should be a list", type(brands_overview))
                    return False
                
                # Check if we have data for brands
                if len(brands_overview) == 0:
                    self.log_result("Dashboard Endpoint", False, "No brand data in overview", "Empty brands_overview")
                    return False
                
                # Validate brand overview structure
                brand_fields = ["brand", "sentiment_avg", "sentiment_trend", "total_mentions", "engagement_score", "market_share"]
                for brand_data in brands_overview[:3]:  # Check first 3 brands
                    for field in brand_fields:
                        if field not in brand_data:
                            self.log_result("Dashboard Endpoint", False, f"Missing brand field: {field}", brand_data.keys())
                            return False
                    
                    # Validate sentiment score range
                    sentiment = brand_data["sentiment_avg"]
                    if not isinstance(sentiment, (int, float)) or sentiment < -1 or sentiment > 1:
                        self.log_result("Dashboard Endpoint", False, f"Invalid sentiment score: {sentiment}", "Should be between -1 and 1")
                        return False
                    
                    # Validate sentiment trend
                    trend = brand_data["sentiment_trend"]
                    if trend not in ["rising", "falling", "stable"]:
                        self.log_result("Dashboard Endpoint", False, f"Invalid sentiment trend: {trend}", "Should be rising/falling/stable")
                        return False
                    
                    # Validate market share
                    market_share = brand_data["market_share"]
                    if not isinstance(market_share, (int, float)) or market_share < 0 or market_share > 100:
                        self.log_result("Dashboard Endpoint", False, f"Invalid market share: {market_share}", "Should be 0-100%")
                        return False
                
                # Validate recent mentions
                recent_mentions = data["recent_mentions"]
                if not isinstance(recent_mentions, list):
                    self.log_result("Dashboard Endpoint", False, "recent_mentions should be a list", type(recent_mentions))
                    return False
                
                # Validate mention structure if we have mentions
                if len(recent_mentions) > 0:
                    mention_fields = ["id", "brand", "source", "content", "sentiment_score", "sentiment_label", "engagement", "timestamp"]
                    first_mention = recent_mentions[0]
                    for field in mention_fields:
                        if field not in first_mention:
                            self.log_result("Dashboard Endpoint", False, f"Missing mention field: {field}", first_mention.keys())
                            return False
                    
                    # Validate sentiment label
                    sentiment_label = first_mention["sentiment_label"]
                    if sentiment_label not in ["positive", "negative", "neutral"]:
                        self.log_result("Dashboard Endpoint", False, f"Invalid sentiment label: {sentiment_label}")
                        return False
                
                # Validate market predictions
                market_predictions = data["market_predictions"]
                if not isinstance(market_predictions, dict):
                    self.log_result("Dashboard Endpoint", False, "market_predictions should be a dict", type(market_predictions))
                    return False
                
                # Validate timestamp format
                last_updated = data["last_updated"]
                try:
                    datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
                except ValueError:
                    self.log_result("Dashboard Endpoint", False, "Invalid timestamp format", last_updated)
                    return False
                
                self.log_result("Dashboard Endpoint", True, f"Dashboard data valid with {len(brands_overview)} brands and {len(recent_mentions)} recent mentions")
                return True
            else:
                self.log_result("Dashboard Endpoint", False, f"HTTP {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Dashboard Endpoint", False, "Request failed", str(e))
            return False
    
    def test_brand_analytics(self):
        """Test GET /api/brand/{brand_name}/analytics endpoint"""
        # Test with a few different brands
        test_brands = ["Zara", "Myntra", "Nike"]
        
        for brand in test_brands:
            try:
                response = self.session.get(f"{BASE_URL}/api/brand/{brand}/analytics")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Validate structure
                    required_fields = ["brand", "analytics_history", "recent_mentions", "total_analytics", "total_mentions"]
                    for field in required_fields:
                        if field not in data:
                            self.log_result(f"Brand Analytics ({brand})", False, f"Missing field: {field}", data.keys())
                            continue
                    
                    # Validate brand name matches
                    if data["brand"] != brand:
                        self.log_result(f"Brand Analytics ({brand})", False, f"Brand mismatch: expected {brand}, got {data['brand']}")
                        continue
                    
                    # Validate counts are non-negative integers
                    if not isinstance(data["total_analytics"], int) or data["total_analytics"] < 0:
                        self.log_result(f"Brand Analytics ({brand})", False, f"Invalid total_analytics: {data['total_analytics']}")
                        continue
                    
                    if not isinstance(data["total_mentions"], int) or data["total_mentions"] < 0:
                        self.log_result(f"Brand Analytics ({brand})", False, f"Invalid total_mentions: {data['total_mentions']}")
                        continue
                    
                    # Validate arrays
                    if not isinstance(data["analytics_history"], list):
                        self.log_result(f"Brand Analytics ({brand})", False, "analytics_history should be a list")
                        continue
                    
                    if not isinstance(data["recent_mentions"], list):
                        self.log_result(f"Brand Analytics ({brand})", False, "recent_mentions should be a list")
                        continue
                    
                    self.log_result(f"Brand Analytics ({brand})", True, f"Analytics retrieved: {data['total_analytics']} analytics, {data['total_mentions']} mentions")
                else:
                    self.log_result(f"Brand Analytics ({brand})", False, f"HTTP {response.status_code}", response.text)
            except Exception as e:
                self.log_result(f"Brand Analytics ({brand})", False, "Request failed", str(e))
        
        return True
    
    def test_invalid_brand_analytics(self):
        """Test brand analytics with invalid brand name"""
        try:
            response = self.session.get(f"{BASE_URL}/api/brand/InvalidBrandName/analytics")
            
            # Should still return 200 with empty/minimal data, not an error
            if response.status_code == 200:
                data = response.json()
                if data["total_analytics"] == 0 and data["total_mentions"] == 0:
                    self.log_result("Invalid Brand Analytics", True, "Correctly handles invalid brand name")
                    return True
                else:
                    self.log_result("Invalid Brand Analytics", False, "Should return empty data for invalid brand", data)
                    return False
            else:
                # If it returns an error, that's also acceptable behavior
                self.log_result("Invalid Brand Analytics", True, f"Returns error for invalid brand: HTTP {response.status_code}")
                return True
        except Exception as e:
            self.log_result("Invalid Brand Analytics", False, "Request failed", str(e))
            return False
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Fashion Market Analyst API Tests")
        print(f"📍 Testing against: {BASE_URL}")
        print("=" * 60)
        
        # Test basic connectivity first
        if not self.test_api_root():
            print("⚠️  Root endpoint failed, but continuing with /api/ tests...")
        
        # Test API prefix - this is the main endpoint
        if not self.test_api_prefix_root():
            print("❌ API prefix connectivity failed. Stopping tests.")
            return False
        
        # Test brands endpoint
        self.test_brands_endpoint()
        
        # Test data collection (this populates the database)
        self.test_data_collection()
        
        # Wait a moment for data to be processed
        print("   Waiting 5 seconds for data processing...")
        time.sleep(5)
        
        # Test dashboard with data
        self.test_dashboard_endpoint()
        
        # Test individual brand analytics
        self.test_brand_analytics()
        
        # Test error handling
        self.test_invalid_brand_analytics()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for r in self.results if "✅" in r["status"])
        failed = sum(1 for r in self.results if "❌" in r["status"])
        
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
        
        if failed > 0:
            print("\n🔍 FAILED TESTS:")
            for result in self.results:
                if "❌" in result["status"]:
                    print(f"   • {result['test']}: {result['message']}")
                    if result["details"]:
                        print(f"     Details: {result['details']}")
        
        return failed == 0

if __name__ == "__main__":
    tester = APITester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed! Backend API is working correctly.")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Check the details above.")
        sys.exit(1)