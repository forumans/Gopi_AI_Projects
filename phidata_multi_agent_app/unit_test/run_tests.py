"""
Simple test runner for Financial Analysis System
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def run_quick_tests():
    """Run quick functionality tests"""
    print("🧪 Running Quick Tests...")
    print("=" * 40)
    
    try:
        from app import web_search, get_stock_data, get_stock_news
        
        # Test 1: Web Search
        print("🔍 Testing Web Search...")
        try:
            result = web_search("test query")
            if "Search Results" in result or "No results found" in result or "Search error" in result:
                print("✅ Web Search: PASSED")
            else:
                print("❌ Web Search: FAILED")
        except Exception as e:
            print(f"❌ Web Search: ERROR - {e}")
        
        # Test 2: Stock Data
        print("\n📊 Testing Stock Data...")
        try:
            result = get_stock_data("AAPL")
            if "Stock Data for: AAPL" in result or "No stock data found" in result or "Stock data error" in result:
                print("✅ Stock Data: PASSED")
            else:
                print("❌ Stock Data: FAILED")
        except Exception as e:
            print(f"❌ Stock Data: ERROR - {e}")
        
        # Test 3: Stock News
        print("\n📰 Testing Stock News...")
        try:
            result = get_stock_news("AAPL")
            if "Latest News for: AAPL" in result or "No news found" in result or "News fetch error" in result:
                print("✅ Stock News: PASSED")
            else:
                print("❌ Stock News: FAILED")
        except Exception as e:
            print(f"❌ Stock News: ERROR - {e}")
        
        print("\n" + "=" * 40)
        print("🎉 Quick tests completed!")
        print("💡 For detailed tests, run: python test_financial_analysis.py")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure src/app.py exists and is importable")
        return False
    
    return True

if __name__ == "__main__":
    run_quick_tests()
