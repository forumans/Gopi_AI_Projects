"""
Financial Analysis System - Clean, Production-Ready Version
"""

import gradio as gr
import yfinance as yf
from ddgs import DDGS

def web_search(query):
    """Simple web search using DuckDuckGo"""
    try:
        with DDGS() as ddgs:
            results = []
            for result in ddgs.text(query, max_results=5):
                results.append({
                    "title": result.get("title", ""),
                    "body": result.get("body", ""),
                    "href": result.get("href", "")
                })
            
            if results:
                response = f"🔍 **Search Results for: '{query}'**\n\n"
                for i, item in enumerate(results, 1):
                    response += f"**{i}. {item['title']}**\n"
                    response += f"{item['body'][:200]}...\n"
                    response += f"🔗 [Link]({item['href']})\n\n"
                response += f"📊 Found {len(results)} results"
                return response
            else:
                return f"❌ No results found for: '{query}'\n💡 Try different keywords"
                
    except Exception as e:
        return f"❌ Search error: {str(e)}\n💡 Check internet connection and try again"

def get_stock_data(symbol):
    """Get stock data using Yahoo Finance"""
    try:
        stock = yf.Ticker(symbol.upper())
        
        # Get current price
        info = stock.info
        current_price = info.get('currentPrice', info.get('regularMarketPrice'))
        
        # Get historical data for different periods
        hist_1y = stock.history(period="1y")  # 1 year for 52-week data
        hist_ytd = stock.history(period="ytd")   # Year to date
        
        if current_price:
            response = f"📊 **Stock Data for: {symbol.upper()}**\n\n"
            response += f"💰 **Current Price**: ${current_price}"
            
            # 52-week high and low (using 1 year data)
            if not hist_1y.empty:
                week_52_high = hist_1y['High'].max()
                week_52_low = hist_1y['Low'].min()
                response += f"\n\n📅 **52-Week Range**:\n"
                response += f"📈 **52-Week High**: ${week_52_high:.2f}\n"
                response += f"📉 **52-Week Low**: ${week_52_low:.2f}"
            
            # Year-to-date high and low
            if not hist_ytd.empty:
                ytd_high = hist_ytd['High'].max()
                ytd_low = hist_ytd['Low'].min()
                ytd_change = ((hist_ytd['Close'].iloc[-1] - hist_ytd['Close'].iloc[0]) / hist_ytd['Close'].iloc[0]) * 100
                
                response += f"\n\n📅 **Year-to-Date**:\n"
                response += f"📈 **YTD High**: ${ytd_high:.2f}\n"
                response += f"📉 **YTD Low**: ${ytd_low:.2f}\n"
                response += f"🔄 **YTD Change**: {ytd_change:.2f}%"
            
            # Previous close for reference
            prev_close = info.get('previousClose')
            if prev_close:
                response += f"\n\n🔄 **Previous Close**: ${prev_close}"
            
            return response
        else:
            return f"❌ No stock data found for {symbol.upper()}\n💡 Verify the stock symbol is correct"
        
    except Exception as e:
        return f"❌ Stock data error: {str(e)}\n💡 Verify symbol '{symbol}' is correct"

def get_stock_news(symbol):
    """Get stock news using Yahoo Finance"""
    try:
        stock = yf.Ticker(symbol.upper())
        news = stock.news
        
        if news and len(news) > 0:
            response = f"📰 **Latest News for: {symbol.upper()}**\n\n"
            for i, article in enumerate(news[:3], 1):
                title = article.get('title', '')
                publisher = article.get('publisher', '')
                pub_time = article.get('providerPublishTime', '')
                summary = article.get('summary', '')
                
                # Only include articles with actual content
                if title and publisher:
                    # Format the date if it's a timestamp
                    if isinstance(pub_time, (int, float)):
                        import datetime
                        pub_time = datetime.datetime.fromtimestamp(pub_time/1000).strftime('%Y-%m-%d')
                    
                    response += f"**{i}. {title}**\n"
                    response += f"📰 {publisher}\n"
                    response += f"📅 {pub_time}\n"
                    if summary:
                        response += f"📝 {summary[:200]}...\n\n"
                    else:
                        response += "\n"
            
            if response.count('\n\n') > 1:  # Check if we found real news
                return response
            else:
                return f"❌ No news data available for {symbol.upper()}\n💡 Try searching for '{symbol.upper()} news' in the Web Search tab"
        else:
            return f"❌ No news found for {symbol.upper()}\n💡 Try searching for '{symbol.upper()} news' in the Web Search tab"
            
    except Exception as e:
        return f"❌ News fetch error: {str(e)}\n💡 Try searching for '{symbol.upper()} news' in the Web Search tab"

def create_ui():
    """Create simple Gradio UI"""
    
    with gr.Blocks(title="Financial Analysis System") as demo:
        gr.Markdown("# 🤖 Financial Analysis System")
        gr.Markdown("Real-time stock data and web search")
        
        with gr.Tabs():
            # Web Search Tab
            with gr.TabItem("🔍 Web Search"):
                query = gr.Textbox(
                    label="Search Query",
                    placeholder="Enter search query...",
                    lines=2
                )
                search_btn = gr.Button("Search", variant="primary")
                search_output = gr.Textbox(
                    label="Results",
                    lines=10,
                    interactive=False
                )
            
            # Stock Analysis Tab
            with gr.TabItem("📊 Stock Analysis"):
                symbol = gr.Textbox(
                    label="Stock Symbol",
                    placeholder="e.g., AAPL, GOOGL, TSLA",
                    max_lines=1
                )
                
                with gr.Row():
                    stock_btn = gr.Button("Get Stock Data", variant="primary")
                    news_btn = gr.Button("Get News", variant="secondary")
                
                stock_output = gr.Textbox(
                    label="Results",
                    lines=12,
                    interactive=False
                )
        
        # Event handlers
        search_btn.click(web_search, inputs=[query], outputs=[search_output])
        stock_btn.click(get_stock_data, inputs=[symbol], outputs=[stock_output])
        news_btn.click(get_stock_news, inputs=[symbol], outputs=[stock_output])
        
        # Examples
        gr.Examples(
            examples=[
                ["Capital One stock"],
                ["Tesla news"],
                ["Apple stock price"],
                ["AI trends"]
            ],
            inputs=[query],
            outputs=[search_output],
            fn=web_search
        )
        
        gr.Examples(
            examples=[["AAPL"], ["GOOGL"], ["TSLA"], ["MSFT"]],
            inputs=[symbol],
            outputs=[stock_output],
            fn=get_stock_data
        )
    
    return demo

if __name__ == "__main__":
    print("🚀 Starting Financial Analysis System...")
    print("📍 Production-ready version")
    
    demo = create_ui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
