"""
End-to-End UI Tests for Financial Analysis System
Tests the complete user interface workflow from start to finish
"""

import sys
import os
import time
import asyncio
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright, expect

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestUIEndToEnd:
    """End-to-end UI testing for Financial Analysis System"""
    
    def __init__(self):
        """Initialize test environment"""
        self.base_url = "http://localhost:7860"
        self.browser = None
        self.page = None
        self.wait_timeout = 10000  # 10 seconds in milliseconds
    
    def setUp(self):
        """Set up test environment"""
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=True)
            self.page = self.browser.new_page()
            self.page.goto(self.base_url)
            self.page.wait_for_load_state("networkidle")
        except Exception as e:
            print(f"❌ Failed to initialize browser: {e}")
            raise
    
    def tearDown(self):
        """Clean up test environment"""
        if self.browser:
            self.browser.close()
        if hasattr(self, 'playwright'):
            self.playwright.stop()
    
    def test_page_load(self):
        """Test that main page loads correctly"""
        try:
            # Check page title
            title = self.page.title()
            assert "Financial Analysis System" in title, f"Page title incorrect: {title}"
            
            # Check main elements are present
            main_heading = self.page.locator("h1:has-text('Financial Analysis System')")
            expect(main_heading).to_be_visible()
            
            # Check tabs are present
            web_search_tab = self.page.locator("button:has-text('Web Search')")
            stock_analysis_tab = self.page.locator("button:has-text('Stock Analysis')")
            
            expect(web_search_tab).to_be_visible()
            expect(stock_analysis_tab).to_be_visible()
            
            print("✅ Page load test: PASSED")
            return True
            
        except Exception as e:
            print(f"❌ Page load test: FAILED - {e}")
            return False
    
    def test_web_search_workflow(self):
        """Test complete web search workflow"""
        try:
            # Click on Web Search tab
            web_search_tab = self.page.locator("button:has-text('Web Search')")
            expect(web_search_tab).to_be_visible()
            web_search_tab.click()
            
            # Find search input
            search_input = self.page.locator("textarea[placeholder='Enter search query...']")
            expect(search_input).to_be_visible()
            
            # Enter search query
            test_query = "Apple stock price"
            search_input.fill(test_query)
            
            # Click search button
            search_button = self.page.locator("button:has-text('Search')")
            search_button.click()
            
            # Wait for results
            results_area = self.page.locator("textarea[label='Results']")
            expect(results_area).to_contain_text("Search Results", timeout=self.wait_timeout)
            
            # Check results content
            results_text = results_area.input_value()
            
            assert "Search Results" in results_text, "Search results not found"
            assert "Apple" in results_text or "stock" in results_text.lower(), "Search content not found"
            
            print("✅ Web search workflow test: PASSED")
            return True
            
        except Exception as e:
            print(f"❌ Web search workflow test: FAILED - {e}")
            return False
    
    def test_stock_analysis_workflow(self):
        """Test complete stock analysis workflow"""
        try:
            # Click on Stock Analysis tab
            stock_tab = self.page.locator("button:has-text('Stock Analysis')")
            expect(stock_tab).to_be_visible()
            stock_tab.click()
            
            # Find stock symbol input
            symbol_input = self.page.locator("input[placeholder='e.g., AAPL, GOOGL, TSLA']")
            expect(symbol_input).to_be_visible()
            
            # Enter stock symbol
            test_symbol = "AAPL"
            symbol_input.fill(test_symbol)
            
            # Click Get Stock Data button
            stock_button = self.page.locator("button:has-text('Get Stock Data')")
            stock_button.click()
            
            # Wait for results
            results_area = self.page.locator("textarea[label='Results']")
            expect(results_area).to_contain_text("Stock Data for:", timeout=self.wait_timeout)
            
            # Check stock data results
            results_text = results_area.input_value()
            
            assert "Stock Data for: AAPL" in results_text, "Stock data header not found"
            assert "Current Price" in results_text, "Current price not found"
            assert "52-Week" in results_text, "52-week data not found"
            assert "Year-to-Date" in results_text, "YTD data not found"
            
            print("✅ Stock analysis workflow test: PASSED")
            return True
            
        except Exception as e:
            print(f"❌ Stock analysis workflow test: FAILED - {e}")
            return False
    
    def test_stock_news_workflow(self):
        """Test stock news workflow"""
        try:
            # Ensure we're on Stock Analysis tab
            stock_tab = self.page.locator("button:has-text('Stock Analysis')")
            if not stock_tab.is_visible():
                stock_tab.click()
            
            # Find stock symbol input
            symbol_input = self.page.locator("input[placeholder='e.g., AAPL, GOOGL, TSLA']")
            expect(symbol_input).to_be_visible()
            
            # Enter stock symbol
            test_symbol = "AAPL"
            symbol_input.fill(test_symbol)
            
            # Click Get News button
            news_button = self.page.locator("button:has-text('Get News')")
            news_button.click()
            
            # Wait for results
            results_area = self.page.locator("textarea[label='Results']")
            expect(results_area).to_contain_text("Latest News for:", timeout=self.wait_timeout)
            
            # Check news results
            results_text = results_area.input_value()
            
            assert "Latest News for: AAPL" in results_text, "News header not found"
            
            print("✅ Stock news workflow test: PASSED")
            return True
            
        except Exception as e:
            print(f"❌ Stock news workflow test: FAILED - {e}")
            return False
    
    def test_example_buttons(self):
        """Test example buttons functionality"""
        try:
            # Test web search examples
            web_search_tab = self.page.locator("button:has-text('Web Search')")
            expect(web_search_tab).to_be_visible()
            web_search_tab.click()
            
            # Find and click first example
            example_button = self.page.locator("button:has-text('Capital One stock')")
            expect(example_button).to_be_visible()
            example_button.click()
            
            # Wait for search to execute
            self.page.wait_for_timeout(3000)  # 3 seconds
            
            # Check if search was triggered
            search_input = self.page.locator("textarea[placeholder='Enter search query...']")
            expect(search_input).to_have_value("Capital One stock")
            
            print("✅ Example buttons test: PASSED")
            return True
            
        except Exception as e:
            print(f"❌ Example buttons test: FAILED - {e}")
            return False
    
    def test_error_handling(self):
        """Test error handling in UI"""
        try:
            # Test invalid stock symbol
            stock_tab = self.page.locator("button:has-text('Stock Analysis')")
            expect(stock_tab).to_be_visible()
            stock_tab.click()
            
            symbol_input = self.page.locator("input[placeholder='e.g., AAPL, GOOGL, TSLA']")
            expect(symbol_input).to_be_visible()
            
            symbol_input.fill("INVALIDSYMBOL")
            
            stock_button = self.page.locator("button:has-text('Get Stock Data')")
            stock_button.click()
            
            # Wait for error response
            self.page.wait_for_timeout(3000)
            
            results_area = self.page.locator("textarea[label='Results']")
            results_text = results_area.input_value()
            
            assert "No stock data found" in results_text or "Stock data error" in results_text, "Error message not displayed"
            
            print("✅ Error handling test: PASSED")
            return True
            
        except Exception as e:
            print(f"❌ Error handling test: FAILED - {e}")
            return False
    
    def test_responsive_design(self):
        """Test responsive design elements"""
        try:
            # Test mobile size
            self.page.set_viewport_size({"width": 375, "height": 667})  # iPhone size
            
            # Check elements are still visible
            main_heading = self.page.locator("h1:has-text('Financial Analysis System')")
            expect(main_heading).to_be_visible()
            
            # Test tablet size
            self.page.set_viewport_size({"width": 768, "height": 1024})  # iPad size
            expect(main_heading).to_be_visible()
            
            # Test desktop size
            self.page.set_viewport_size({"width": 1920, "height": 1080})
            expect(main_heading).to_be_visible()
            
            print("✅ Responsive design test: PASSED")
            return True
            
        except Exception as e:
            print(f"❌ Responsive design test: FAILED - {e}")
            return False
    
    def test_accessibility(self):
        """Test basic accessibility features"""
        try:
            # Test keyboard navigation
            self.page.keyboard.press("Tab")
            self.page.keyboard.press("Tab")
            
            # Check if focus moves to interactive elements
            focused_element = self.page.locator(":focus")
            expect(focused_element).to_be_visible()
            
            # Test ARIA labels
            search_input = self.page.locator("textarea[placeholder='Enter search query...']")
            expect(search_input).to_have_attribute("aria-label")
            
            print("✅ Accessibility test: PASSED")
            return True
            
        except Exception as e:
            print(f"❌ Accessibility test: FAILED - {e}")
            return False


class TestRunner:
    """Test runner for E2E tests"""
    
    def __init__(self):
        self.test_instance = TestUIEndToEnd()
    
    def check_server_running(self):
        """Check if the application server is running"""
        try:
            import requests
            response = requests.get("http://localhost:7860", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def run_all_tests(self):
        """Run all E2E tests"""
        print("🌐 Running End-to-End UI Tests...")
        print("=" * 50)
        
        # Check if server is running
        if not self.check_server_running():
            print("❌ Server not running on http://localhost:7860")
            print("💡 Start the server first: python main.py")
            return False
        
        test_results = []
        
        try:
            # Set up test environment
            self.test_instance.setUp()
            
            # Run all tests
            tests = [
                ("Page Load", self.test_instance.test_page_load),
                ("Web Search Workflow", self.test_instance.test_web_search_workflow),
                ("Stock Analysis Workflow", self.test_instance.test_stock_analysis_workflow),
                ("Stock News Workflow", self.test_instance.test_stock_news_workflow),
                ("Example Buttons", self.test_instance.test_example_buttons),
                ("Error Handling", self.test_instance.test_error_handling),
                ("Responsive Design", self.test_instance.test_responsive_design)
            ]
            
            for test_name, test_func in tests:
                print(f"\n🧪 Running {test_name} Test...")
                try:
                    result = test_func()
                    test_results.append((test_name, result))
                except Exception as e:
                    print(f"❌ {test_name} Test: EXCEPTION - {e}")
                    test_results.append((test_name, False))
            
            # Clean up
            self.test_instance.tearDown()
            
        except Exception as e:
            print(f"❌ Test setup failed: {e}")
            return False
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 E2E Test Results Summary:")
        
        passed = sum(1 for _, result in test_results if result)
        total = len(test_results)
        
        print(f"   Tests run: {total}")
        print(f"   Passed: {passed}")
        print(f"   Failed: {total - passed}")
        print(f"   Success rate: {(passed/total)*100:.1f}%")
        
        failed_tests = [name for name, result in test_results if not result]
        if failed_tests:
            print(f"\n❌ Failed Tests:")
            for test_name in failed_tests:
                print(f"   - {test_name}")
        else:
            print(f"\n✅ All E2E tests passed!")
        
        return passed == total


def run_e2e_tests():
    """Main function to run E2E tests"""
    print("🌐 Financial Analysis System - End-to-End UI Tests")
    print("📍 Testing complete user workflows")
    
    runner = TestRunner()
    success = runner.run_all_tests()
    
    if success:
        print("\n🎉 All E2E tests completed successfully!")
        print("💡 Application is ready for production deployment")
    else:
        print("\n⚠️  Some E2E tests failed")
        print("💡 Check the application functionality before deployment")
    
    return success


if __name__ == "__main__":
    run_e2e_tests()
