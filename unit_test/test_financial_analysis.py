"""
Unit Tests for Financial Analysis System
Tests all core functionality: web search, stock data, and stock news
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import web_search, get_stock_data, get_stock_news

class TestFinancialAnalysis(unittest.TestCase):
    """Test suite for Financial Analysis System"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_query = "Apple stock price"
        self.test_symbol = "AAPL"
    
    def test_web_search_success(self):
        """Test successful web search"""
        with patch('app.DDGS') as mock_ddgs:
            # Mock DuckDuckGo response
            mock_result = MagicMock()
            mock_result.get.side_effect = lambda key, default="": {
                "title": "Apple Stock Price",
                "body": "Latest Apple stock price information",
                "href": "https://example.com/apple"
            }.get(key, default)
            
            mock_ddgs.return_value.__enter__.return_value.text.return_value = [mock_result]
            
            result = web_search(self.test_query)
            
            # Assertions
            self.assertIn("Search Results", result)
            self.assertIn("Apple Stock Price", result)
            self.assertIn("Found 1 results", result)
            self.assertIn("🔗", result)
    
    def test_web_search_no_results(self):
        """Test web search with no results"""
        with patch('app.DDGS') as mock_ddgs:
            mock_ddgs.return_value.__enter__.return_value.text.return_value = []
            
            result = web_search(self.test_query)
            
            # Assertions
            self.assertIn("No results found", result)
            self.assertIn("Try different keywords", result)
    
    def test_web_search_exception(self):
        """Test web search with exception"""
        with patch('app.DDGS') as mock_ddgs:
            mock_ddgs.side_effect = Exception("Connection error")
            
            result = web_search(self.test_query)
            
            # Assertions
            self.assertIn("Search error", result)
            self.assertIn("Check internet connection", result)
    
    def test_get_stock_data_success(self):
        """Test successful stock data retrieval"""
        with patch('app.yf.Ticker') as mock_ticker:
            # Mock Yahoo Finance response
            mock_info = {
                'currentPrice': 182.52,
                'dayHigh': 184.20,
                'dayLow': 181.30,
                'previousClose': 183.85
            }
            
            # Mock historical data
            import pandas as pd
            mock_hist_1y = pd.DataFrame({
                'High': [199.62, 195.50, 190.25],
                'Low': [164.08, 168.20, 172.50],
                'Close': [170.50, 175.25, 182.52]
            })
            
            mock_hist_ytd = pd.DataFrame({
                'High': [199.62, 195.50],
                'Low': [164.08, 168.20],
                'Close': [170.50, 182.52]
            })
            
            mock_stock = MagicMock()
            mock_stock.info = mock_info
            mock_stock.history.side_effect = lambda period: (
                mock_hist_1y if period == "1y" else mock_hist_ytd
            )
            mock_ticker.return_value = mock_stock
            
            result = get_stock_data(self.test_symbol)
            
            # Assertions
            self.assertIn("Stock Data for: AAPL", result)
            self.assertIn("Current Price: $182.52", result)
            self.assertIn("52-Week High", result)
            self.assertIn("52-Week Low", result)
            self.assertIn("YTD High", result)
            self.assertIn("YTD Low", result)
            self.assertIn("YTD Change", result)
            self.assertIn("Previous Close: $183.85", result)
    
    def test_get_stock_data_no_price(self):
        """Test stock data with no current price"""
        with patch('app.yf.Ticker') as mock_ticker:
            mock_stock = MagicMock()
            mock_stock.info = {'currentPrice': None}
            mock_ticker.return_value = mock_stock
            
            result = get_stock_data(self.test_symbol)
            
            # Assertions
            self.assertIn("No stock data found", result)
            self.assertIn("Verify stock symbol", result)
    
    def test_get_stock_data_exception(self):
        """Test stock data with exception"""
        with patch('app.yf.Ticker') as mock_ticker:
            mock_ticker.side_effect = Exception("API error")
            
            result = get_stock_data(self.test_symbol)
            
            # Assertions
            self.assertIn("Stock data error", result)
            self.assertIn("Verify symbol", result)
    
    def test_get_stock_news_success(self):
        """Test successful stock news retrieval"""
        with patch('app.yf.Ticker') as mock_ticker:
            # Mock news response
            mock_news = [
                {
                    'title': 'Apple Reports Strong Earnings',
                    'publisher': 'Reuters',
                    'providerPublishTime': 1709070400000,  # Mock timestamp
                    'summary': 'Apple Inc. reported better than expected earnings...'
                },
                {
                    'title': 'Apple Stock Rises on New Products',
                    'publisher': 'Bloomberg',
                    'providerPublishTime': 1708984000000,
                    'summary': 'Apple shares increased following new product announcements...'
                }
            ]
            
            mock_stock = MagicMock()
            mock_stock.news = mock_news
            mock_ticker.return_value = mock_stock
            
            result = get_stock_news(self.test_symbol)
            
            # Assertions
            self.assertIn("Latest News for: AAPL", result)
            self.assertIn("Apple Reports Strong Earnings", result)
            self.assertIn("Reuters", result)
            self.assertIn("Bloomberg", result)
            self.assertIn("2024-02-28", result)  # Formatted date
            self.assertIn("better than expected earnings", result)
    
    def test_get_stock_news_no_articles(self):
        """Test stock news with no articles"""
        with patch('app.yf.Ticker') as mock_ticker:
            mock_stock = MagicMock()
            mock_stock.news = []
            mock_ticker.return_value = mock_stock
            
            result = get_stock_news(self.test_symbol)
            
            # Assertions
            self.assertIn("No news found", result)
            self.assertIn("Try searching for 'AAPL news'", result)
    
    def test_get_stock_news_exception(self):
        """Test stock news with exception"""
        with patch('app.yf.Ticker') as mock_ticker:
            mock_ticker.side_effect = Exception("News API error")
            
            result = get_stock_news(self.test_symbol)
            
            # Assertions
            self.assertIn("News fetch error", result)
            self.assertIn("Try searching for 'AAPL news'", result)
    
    def test_get_stock_news_invalid_articles(self):
        """Test stock news with invalid articles (no title/publisher)"""
        with patch('app.yf.Ticker') as mock_ticker:
            # Mock news with invalid articles
            mock_news = [
                {'title': '', 'publisher': 'Reuters', 'summary': 'Valid article'},
                {'title': 'Valid Title', 'publisher': '', 'summary': 'Valid article'},
                {'title': 'Valid Title', 'publisher': 'Bloomberg', 'summary': 'Valid article'}
            ]
            
            mock_stock = MagicMock()
            mock_stock.news = mock_news
            mock_ticker.return_value = mock_stock
            
            result = get_stock_news(self.test_symbol)
            
            # Assertions - should only include valid article
            self.assertIn("Latest News for: AAPL", result)
            self.assertIn("Valid Title", result)
            self.assertIn("Bloomberg", result)
            # Should not include empty title or publisher articles
            self.assertNotIn("Valid article", result.count("Valid article"))  # Should only appear once
    
    def test_input_validation(self):
        """Test input validation for edge cases"""
        # Test empty inputs
        with patch('app.DDGS') as mock_ddgs:
            mock_ddgs.return_value.__enter__.return_value.text.return_value = []
            
            result = web_search("")
            self.assertIn("No results found", result)
        
        with patch('app.yf.Ticker') as mock_ticker:
            mock_stock = MagicMock()
            mock_stock.info = {'currentPrice': None}
            mock_ticker.return_value = mock_stock
            
            result = get_stock_data("")
            self.assertIn("No stock data found", result)
    
    def test_output_formatting(self):
        """Test that outputs are properly formatted"""
        with patch('app.DDGS') as mock_ddgs:
            mock_result = MagicMock()
            mock_result.get.side_effect = lambda key, default="": {
                "title": "Test Result",
                "body": "Test description",
                "href": "https://test.com"
            }.get(key, default)
            
            mock_ddgs.return_value.__enter__.return_value.text.return_value = [mock_result]
            
            result = web_search("test query")
            
            # Check formatting elements
            self.assertIn("🔍", result)  # Emoji present
            self.assertIn("**", result)  # Markdown formatting
            self.assertIn("🔗", result)  # Link emoji
            self.assertIn("📊", result)  # Results emoji


class TestIntegration(unittest.TestCase):
    """Integration tests for combined functionality"""
    
    def test_symbol_case_insensitivity(self):
        """Test that stock symbols work regardless of case"""
        with patch('app.yf.Ticker') as mock_ticker:
            mock_stock = MagicMock()
            mock_stock.info = {'currentPrice': 100.0}
            mock_stock.history.return_value = MagicMock()
            mock_ticker.return_value = mock_stock
            
            # Test different cases
            result_upper = get_stock_data("AAPL")
            result_lower = get_stock_data("aapl")
            result_mixed = get_stock_data("AaPl")
            
            # All should work (yf.Ticker should be called with uppercase)
            self.assertEqual(mock_ticker.call_count, 3)
            self.assertEqual(mock_ticker.call_args_list[0][0][0], "AAPL")
            self.assertEqual(mock_ticker.call_args_list[1][0][0], "AAPL")
            self.assertEqual(mock_ticker.call_args_list[2][0][0], "AAPL")
    
    def test_error_message_consistency(self):
        """Test that error messages follow consistent format"""
        with patch('app.DDGS') as mock_ddgs:
            mock_ddgs.side_effect = Exception("Test error")
            
            result = web_search("test")
            
            # Check error message format
            self.assertTrue(result.startswith("❌"))
            self.assertIn("💡", result)  # Should have helpful tip


def run_tests():
    """Run all tests and return results"""
    print("🧪 Running Financial Analysis System Tests...")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestFinancialAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("=" * 50)
    print(f"📊 Test Results Summary:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
    print(f"   Success rate: {success_rate:.1f}%")
    
    if result.failures:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback}")
    
    if result.errors:
        print(f"\n🚨 Errors:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback}")
    
    if result.wasSuccessful():
        print(f"\n✅ All tests passed!")
    else:
        print(f"\n❌ Some tests failed!")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
